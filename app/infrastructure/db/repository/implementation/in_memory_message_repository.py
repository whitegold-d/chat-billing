import datetime
from typing import Literal, List
from uuid import uuid4

from app.infrastructure.db.model.request.message_request import MessageRequestORM
from app.infrastructure.db.model.response.message_response import MessageResponseORM
from app.infrastructure.db.repository.interface.base_message_repository import BaseMessageRepository


class InMemoryMessageRepository(BaseMessageRepository):
    messages: List[MessageResponseORM] = []
    _self = None

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    async def get_all_messages(self, **filters):
        if filters is None:
            return self.messages

        result_messages = []
        for key, value in filters.items():
            for message in self.messages:
                if hasattr(message, key):
                    if getattr(message, key) == value:
                        result_messages.append(message)
        return result_messages


    async def create_message(self, data: MessageRequestORM):
        new_message = MessageResponseORM(
            id=uuid4(),
            chat_id=data.chat_id,
            role=data.role,
            text=data.text,
            created_at=datetime.datetime.now()
        )
        self.messages.append(new_message)
        return new_message