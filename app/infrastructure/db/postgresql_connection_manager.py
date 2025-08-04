from contextlib import asynccontextmanager

import asyncpg

from app.utils.constants import PG_DATABASE_DSN


class PostgreSQLConnectionManager:
    _pool = None

    @classmethod
    async def create_pool(cls):
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(PG_DATABASE_DSN, min_size=3, max_size=9)


    @classmethod
    def get_pool(cls):
        if not cls._pool:
            cls.create_pool()
        return cls._pool


    @classmethod
    @asynccontextmanager
    async def get_connection(cls):
        async with cls.get_pool().acquire() as conn:
            yield conn


    @classmethod
    async def close_pool(cls):
        await cls._pool.close()