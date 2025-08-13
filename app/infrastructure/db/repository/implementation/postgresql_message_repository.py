from typing import List

import asyncpg
from sqlalchemy import select, insert

from app.infrastructure.db.model.ORM.message_orm import MessageORM
from app.infrastructure.db.model.request.message_request import MessageRequestORM
from app.infrastructure.db.model.response.message_response import MessageResponseORM
from app.infrastructure.db.postgresql_connection_manager import PostgreSQLConnectionManager
from app.infrastructure.db.repository.interface.base_message_repository import BaseMessageRepository


class PostgreSQLMessageRepository(BaseMessageRepository):
    _self = None

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self


    async def get_all_messages(self) -> List[MessageResponseORM]:
        with PostgreSQLConnectionManager.get_session() as session:
            stmt = select(MessageORM)
            result = await session.execute(stmt)
            messages = result.fetchall()

        result = [MessageResponseORM(*args) for args in messages]
        return result


    async def create_message(self, data: MessageRequestORM) -> MessageResponseORM:
        with PostgreSQLConnectionManager.get_session() as session:
            stmt = insert(MessageORM).values()
        return