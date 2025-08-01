from abc import ABC, abstractmethod

from app.infrastructure.db.model.request.message_request import MessageRequestORM
from app.infrastructure.db.repository.base_repository import BaseRepository


class BaseMessageRepository(ABC, BaseRepository):
    @abstractmethod
    async def get_all_messages(self, **filters):
        raise NotImplementedError

    @abstractmethod
    async def create_message(self, data: MessageRequestORM):
        raise NotImplementedError