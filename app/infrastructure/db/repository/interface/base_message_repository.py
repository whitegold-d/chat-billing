from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.infrastructure.db.model.request.message_request import MessageRequestORM
from app.infrastructure.db.model.response.message_response import MessageResponseORM


class BaseMessageRepository(ABC):
    @abstractmethod
    async def get_all_messages(self) -> List[MessageResponseORM]:
        raise NotImplementedError

    @abstractmethod
    async def create_message(self, data: MessageRequestORM) -> MessageResponseORM:
        raise NotImplementedError

    @abstractmethod
    async def get_messages_by_chat_id(self, chat_id: UUID) -> List[MessageResponseORM]:
        raise NotImplementedError