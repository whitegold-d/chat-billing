from pgvector.asyncpg import register_vector

from app.infrastructure.db.initialize.interface.base_database import BaseDatabase
from app.infrastructure.db.postgresql_connection_manager import PostgreSQLConnectionManager


class PostgreSQLDatabase(BaseDatabase):
    _self = None

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            return super().__new__(cls)
        return cls._self


    async def initialize_db(self) -> None:
        await PostgreSQLConnectionManager.create_pool()

        async with PostgreSQLConnectionManager.get_connection() as conn:
            await conn.execute(
                """
                CREATE EXTENSION IF NOT EXISTS vector;
                """
            )
            await register_vector(conn)
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id UUID PRIMARY KEY,
                    text TEXT NOT NULL,
                    embedding vector(768)
                );
                CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);
                """
            )
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id UUID PRIMARY KEY,
                    login TEXT NOT NULL,
                    name TEXT UNIQUE NOT NULL,
                    hashed_password TEXT NOT NULL);"""
            )
            # await conn.execute(
            #     """
            #     CREATE TYPE transaction_type as ENUM (
            #         'u2u', 'top_up', 'chat'
            #     );
            #     """
            # )
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id UUID PRIMARY KEY,
                    user_id UUID NOT NULL,
                    transaction_type TEXT NOT NULL,
                    value INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id))"""
            )


    async def close_db(self) -> None:
        await PostgreSQLConnectionManager.close_pool()
