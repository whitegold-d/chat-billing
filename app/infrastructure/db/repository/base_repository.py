
from contextlib import asynccontextmanager

import asyncpg


class BaseRepository:
    dsn: str

    @classmethod
    @asynccontextmanager
    async def _get_db_connection(cls):
        conn: asyncpg.connection.Connection = await asyncpg.connect(cls.dsn)
        try:
            yield conn
        finally:
            await conn.close()