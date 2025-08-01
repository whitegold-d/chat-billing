from abc import ABC, abstractmethod
from typing import Literal, List

from app.infrastructure.db.model.request.message_request import MessageRequestORM
from app.infrastructure.db.model.response.message_response import MessageResponseORM


class BaseMessageService(ABC):
    @abstractmethod
    async def get_history(self, chat_id: str,
                          size: int = 20) -> List[MessageResponseORM]:
        raise NotImplementedError

    @abstractmethod
    async def create_message(self, chat_id: str,
                             role: Literal["assistant", "human"],
                             text: str) -> MessageResponseORM:
        raise NotImplementedError