from datetime import datetime
import uuid
from typing import List
from uuid import UUID

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
        async with PostgreSQLConnectionManager.get_session() as session:
            stmt = select(MessageORM)
            result = await session.execute(stmt)
            messages = result.scalars().all()

        result = [MessageResponseORM(id=message.id,
                                     chat_id=message.chat_id,
                                     role=message.role,
                                     text=message.text,
                                     created_at=message.created_at) for message in messages]
        return result


    async def create_message(self, data: MessageRequestORM) -> MessageResponseORM:
        message_id = uuid.uuid4()
        date_now = datetime.now()

        async with PostgreSQLConnectionManager.get_session() as session:
            stmt = insert(MessageORM).values(id=message_id,
                                             chat_id=data.chat_id,
                                             role=data.role,
                                             text=data.text,
                                             created_at=date_now)
            await session.execute(stmt)
            await session.commit()
        return MessageResponseORM(id=message_id,
                                  chat_id=data.chat_id,
                                  role=data.role,
                                  text=data.text,
                                  created_at=date_now)


    async def get_messages_by_chat_id(self, chat_id: UUID) -> List[MessageResponseORM]:
        async with PostgreSQLConnectionManager.get_session() as session:
            stmt = select(MessageORM).where(MessageORM.chat_id == chat_id)
            result = await session.execute(stmt)
            messages = result.scalars().all()

        result = [MessageResponseORM(id=message.id,
                                     chat_id=message.chat_id,
                                     role=message.role,
                                     text=message.text,
                                     created_at=message.created_at) for message in messages]
        return result