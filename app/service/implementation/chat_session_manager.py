from uuid import UUID

from app.rag.rag import RAG
from app.service.interface.base_agent_service import BaseAgentService
from app.service.interface.base_chat_session_manager import BaseChatSessionManager
from app.service.interface.base_llm_service import BaseLLMService
from app.service.interface.base_message_service import BaseMessageService
from app.service.interface.base_transaction_service import BaseTransactionService


class ChatSessionManager(BaseChatSessionManager):
    _self = None
    def __new__(cls, message_service: BaseMessageService,
                tr_service: BaseTransactionService,
                agent_service: BaseAgentService,
                rag_service: RAG):
        if cls._self is None:
            cls._self = super().__new__(cls)
            cls._self.message_service = message_service
            cls._self.tr_service = tr_service
            cls._self.rag_service = rag_service
            cls._self.agent_service = agent_service
        return cls._self

    async def send_message(self, user_id: str, chat_id: str, new_message: str):
        history = await self.message_service.get_history(UUID(str(chat_id)), size=20)
        answer = await self.agent_service.execute(
            text=new_message,
            history=history
        )

        await self.message_service.create_message(chat_id, "human", new_message)
        await self.message_service.create_message(chat_id, "assistant", answer.text)
        await self.tr_service.create_transaction(user_id, "chat", -1 * answer.used_tokens)
        return answer


    async def upload_documents(self, document_url: str):
        await self.rag_service.upload_documents(document_url)


    async def retrieve_information(self, user_query: str, limit: int = 5):
        records = await self.rag_service.vector_search(user_query, limit)
        print(records)


