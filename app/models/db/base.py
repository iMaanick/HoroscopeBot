import os

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def create_pool() -> async_sessionmaker[AsyncSession]:
    db_uri = os.getenv('DATABASE_URI')
    if not db_uri:
        raise ValueError("DATABASE_URI env variable is not set")
    engine = create_async_engine(
        db_uri,
        echo=True, )
    pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    return pool
