from abc import ABC, abstractmethod


class BaseChatSessionManager(ABC):
    @abstractmethod
    async def send_message(self, user_id: str, chat_id: str, new_message: str):
        raise NotImplementedError