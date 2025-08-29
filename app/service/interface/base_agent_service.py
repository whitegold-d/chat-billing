from abc import abstractmethod, ABC
from typing import Sequence
from uuid import UUID

from app.infrastructure.db.model.response.message_response import MessageResponseORM


class BaseAgentService(ABC):
    @abstractmethod
    async def execute(self, text: str, history: Sequence[MessageResponseORM]):
        raise NotImplementedError

