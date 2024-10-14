from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


engine = create_async_engine(settings.db.async_dsn, echo=True)


class Base(DeclarativeBase):
    pass