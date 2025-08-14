from typing import List, Literal
from uuid import UUID

from app.infrastructure.db.model.request.message_request import MessageRequestORM
from app.infrastructure.db.model.response.message_response import MessageResponseORM
from app.infrastructure.db.repository.interface.base_message_repository import BaseMessageRepository
from app.service.interface.base_message_service import BaseMessageService


class MessageService(BaseMessageService):
    _self = None

    def __new__(cls, message_repository: BaseMessageRepository):
        if cls._self is None:
            cls._self = super().__new__(cls)
            cls._self.message_repository = message_repository
        return cls._self


    async def get_history(self, chat_id: UUID, size: int = 20) -> List[MessageResponseORM]:
        result = await self.message_repository.get_messages_by_chat_id(chat_id)
        return result[:size]


    async def create_message(self, chat_id: str, role: Literal["assistant", "human"], text: str) -> MessageResponseORM:
        new_message = await self.message_repository.create_message(
            MessageRequestORM(
                chat_id=chat_id,
                role=role,
                text=text))
        return new_message
