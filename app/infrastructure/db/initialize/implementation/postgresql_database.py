from pgvector.asyncpg import register_vector
from sqlalchemy import text

from app.infrastructure.db.initialize.interface.base_database import BaseDatabase
from app.infrastructure.db.model.ORM.base import Base
from app.infrastructure.db.postgresql_connection_manager import PostgreSQLConnectionManager


class PostgreSQLDatabase(BaseDatabase):
    _self = None

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            return super().__new__(cls)
        return cls._self


    async def initialize_db(self) -> None:
        async with PostgreSQLConnectionManager.get_connection() as conn:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            await register_vector(conn)
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()