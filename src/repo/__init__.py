from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import async_sessionmaker
from uuid import UUID

from src.interfaces import IRepository, ModelType, SchemaType
from src.database import engine

import src.repo.exceptions as exc


class SQARepository(IRepository):
    def __init__(self, model: ModelType):
        self.model = model
        self.session = async_sessionmaker(
            bind=engine, 
            autoflush=False, 
            expire_on_commit=False, 
            autocommit=False
        )
        
    async def add_and_commit(self, db_model: ModelType) -> ModelType:
        async with self.session() as session:
            try:
                session.add(db_model)
                await session.commit()
                await session.refresh(db_model)
                return db_model
            except exc.IntegrityError:
                raise exc.IntegrityConflictError(f"{self.model.__tablename__} conflicts with existing data.")
            except Exception as e:
                raise exc.RepositoryError(f"Неизвестная ошибка: {e}") from e

    async def create(self, schema: SchemaType) -> ModelType | None:
        db_model = self.model(**schema.model_dump())
        try:
            return await self.add_and_commit(db_model)
        except Exception as e:
            raise e

    async def create_many(self, schemas: list[SchemaType]) -> list[ModelType]:
        db_models = [self.model(**schema.model_dump()) for schema in schemas]

        async with self.session() as session:
            try:
                session.add_all(db_models)
                await session.commit()

                for model in db_models:
                    await session.refresh(model)

                return db_models
            except exc.IntegrityError:
                raise exc.IntegrityConflictError(
                    f"{self.model.__tablename__} conflicts with existing data."
                )
            except Exception as e:
                raise exc.RepositoryError(f"Неизвестная ошибка: {e}") from e


    async def get_one_by(self, value: str, column: str, with_for_update: bool = False) -> ModelType | None:
        try:
            query = select(self.model).where(getattr(self.model, column) == value)
        except AttributeError:
            raise exc.RepositoryError(f"Столбец {column} не найде в таблице {self.model.__tablename__}")

        if with_for_update:
            query = query.with_for_update()

        async with self.session() as session:
            results = await session.execute(query)
            return results.unique().scalar_one_or_none()

    async def get_many_by(self, values: list[str | UUID], column: str, with_for_update: bool = False):
        query = select(self.model)
        if values:
            try:
                query = query.where(getattr(self.model, column).in_(values))
            except AttributeError:
                raise exc.RepositoryError(f"Столбец {column} не найде в таблице {self.model.__tablename__}")

        if with_for_update:
            query = query.with_for_update()

        async with self.session() as session:
            rows = await session.execute(query) 
            return rows.unique().scalars().all()

    async def update_one_by(self, data: SchemaType, value: str, column: str) -> ModelType:
        db_model = await self.get_one_by(value=value, column=column, with_for_update=True)

        if not db_model:
            raise exc.NotFoundError(f"{self.model.__tablename__} {column}={value} не найден")

        schema_values = data.model_dump(exclude_unset=True)
        for k, v in schema_values.items():
            setattr(db_model, k, v)

        async with self.session() as session:
            try:
                await session.commit()
                await session.refresh(db_model)
                return db_model
            except exc.IntegrityError:
                raise exc.IntegrityConflictError(
                    f"{self.model.__tablename__} {column}={value} conflicts with existing data."
                )

    async def remove_by(self, value: str, column: str) -> int:
        try:
            query = delete(self.model).where(getattr(self.model, column) == value)
        except AttributeError:
            raise exc.RepositoryError(f"Столбец {column} не найден в таблице {self.model.__tablename__}")
        
        async with self.session() as session:
            rows = await session.execute(query)
            await session.commit()

            return rows.rowcount
