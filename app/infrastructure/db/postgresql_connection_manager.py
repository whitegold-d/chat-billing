from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.utils.settings import Settings


class PostgreSQLConnectionManager:
    _engine = create_async_engine(
        url=Settings().db_dsn,
        echo=True,
        pool_size=10,
    )
    _async_session_local = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

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
