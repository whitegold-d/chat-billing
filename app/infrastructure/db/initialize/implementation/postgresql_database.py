import asyncpg

from app.infrastructure.db.initialize.interface.base_database import BaseDatabase
from app.infrastructure.db.postgresql_connection_manager import PostgreSQLConnectionManager
from app.utils.constants import PG_DATABASE_DSN, DB_PATH

class PostgreSQLDatabase(BaseDatabase):
    _self = None

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            return super().__new__(cls)
        return cls._self


    async def init_db(self) -> None:
        await PostgreSQLConnectionManager.create_pool()

        async with PostgreSQLConnectionManager.get_connection() as conn:
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
                    FOREIGN KEY(user_id) REFERENCES users(id))"""
            )
            print("PostgreSQL database initialized")


    async def close_db(self) -> None:
        await PostgreSQLConnectionManager.close_pool()
