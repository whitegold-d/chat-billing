
from contextlib import asynccontextmanager

import asyncpg

from app.infrastructure.db.initialize.implementation.postgresql_database import pool


class BaseRepository:
    dsn: str

    @classmethod
    @asynccontextmanager
    async def _get_db_connection(cls) -> asyncpg.connection.Connection:
        async with pool.acquire() as conn:
            yield conn