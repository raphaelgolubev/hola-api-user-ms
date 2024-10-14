from abc import ABC, abstractmethod
from typing import TypeAlias
from pydantic import BaseModel

from src.database import Base


ModelType: TypeAlias = Base
SchemaType: TypeAlias = BaseModel


class IRepository(ABC):
    @abstractmethod
    async def add_and_commit(self, db_model: ModelType):
        raise NotImplementedError

    @abstractmethod
    async def create(self, schema: SchemaType):
        raise NotImplementedError

    @abstractmethod
    async def create_many(self, schemas: list[SchemaType]):
        raise NotImplementedError

    @abstractmethod
    async def get_one_by(self, value: str, column: str, with_for_update: bool = False):
        raise NotImplementedError

    @abstractmethod
    async def get_many_by(self, values: list[str], column: str, with_for_update: bool = False):
        raise NotImplementedError

    @abstractmethod
    async def update_one_by(self, data: SchemaType, value: str, column: str):
        raise NotImplementedError

    @abstractmethod
    async def remove_by(self, value: str, column: str):
        raise NotImplementedError


class ISecurity(ABC):
    @abstractmethod
    def hash_value(self, password: str):
        raise NotImplementedError

    @abstractmethod
    def verify(self, plain: str, hash: str):
        raise NotImplementedError
