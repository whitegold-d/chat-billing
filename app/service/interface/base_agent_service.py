from abc import abstractmethod, ABC
from uuid import UUID


class BaseAgentService(ABC):
    @abstractmethod
    async def execute(self, text: str, chat_id: UUID, history_size: int):
        raise NotImplementedError

