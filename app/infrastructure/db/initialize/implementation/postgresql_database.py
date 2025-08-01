import asyncpg

from app.infrastructure.db.initialize.interface.base_database import BaseDatabase
from app.utils.constants import PG_DATABASE_DSN


class PostgreSQLDatabase(BaseDatabase):
    _self = None

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            return super().__new__(cls)
        return cls._self

    async def init_db(self) -> None:
        conn: asyncpg.connection.Connection = await asyncpg.connect(PG_DATABASE_DSN)
        try:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    login TEXT NOT NULL,
                    name TEXT UNIQUE NOT NULL,
                    hashed_password TEXT NOT NULL)"""
            )
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS transaction_model (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    transaction_type TEXT NOT NULL,
                    value INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES user(id))"""
            )
            print("PostgreSQL database initialized")
        finally:
            await conn.close()