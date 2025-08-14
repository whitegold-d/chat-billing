from contextlib import asynccontextmanager

import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.utils.constants import PG_DATABASE_DSN


class PostgreSQLConnectionManager:
    # _pool = None
    _engine = create_async_engine(
        url=PG_DATABASE_DSN,
        echo=True,
        pool_size=10,
    )
    _async_session_local = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # @classmethod
    # async def create_pool(cls):
    #     if cls._pool is None:
    #         cls._pool = await asyncpg.create_pool(PG_DATABASE_DSN, min_size=3, max_size=9)
    #
    #
    # @classmethod
    # def get_pool(cls):
    #     if not cls._pool:
    #         cls.create_pool()
    #     return cls._pool
    #
    # @classmethod
    # async def close_pool(cls):
    #     await cls._pool.close()


    @classmethod
    @asynccontextmanager
    async def get_session(cls):
        async with cls._async_session_local() as session:
            yield session


    @classmethod
    @asynccontextmanager
    async def get_connection(cls):
        async with cls._engine.connect() as connection:
            yield connection
