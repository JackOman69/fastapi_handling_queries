import datetime
from typing import AsyncGenerator

from sqlalchemy import DateTime, MetaData
from sqlalchemy.ext.asyncio import (    
    create_async_engine, 
    async_sessionmaker,
    AsyncAttrs,
    AsyncSession
)
from sqlalchemy.orm import DeclarativeBase

from .settings import SQLALCHEMY_DB_URL


class Base(AsyncAttrs, DeclarativeBase):
    
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s"
        }
    )
    
    type_annotation_map = {
        datetime.datetime: DateTime(timezone=True)
    }
    
engine = create_async_engine(
    SQLALCHEMY_DB_URL,
    echo=True
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session