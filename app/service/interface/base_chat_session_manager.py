from abc import ABC, abstractmethod


class BaseChatSessionManager(ABC):
    @abstractmethod
    async def send_message(self, user_id: str, chat_id: str, new_message: str):
        raise NotImplementedError

    @abstractmethod
    async def upload_documents(self, document_url: str):
        raise NotImplementedError

    @abstractmethod
    async def retrieve_information(self, user_query: str, limit: int):
        raise NotImplementedError