from app.service.interface.base_chat_session_manager import BaseChatSessionManager
from app.service.interface.base_llm_service import BaseLLMService
from app.service.interface.base_message_service import BaseMessageService
from app.service.interface.base_transaction_service import BaseTransactionService


class ChatSessionManager(BaseChatSessionManager):
    _self = None
    def __new__(cls, message_service: BaseMessageService,
                tr_service: BaseTransactionService,
                llm_service: BaseLLMService):
        if cls._self is None:
            cls._self = super().__new__(cls)
            cls._self.message_service = message_service
            cls._self.tr_service = tr_service
            cls._self.llm_service = llm_service
        return cls._self

    async def send_message(self, user_id: str, chat_id: str, new_message: str):
        history = await self.message_service.get_history(chat_id, size=20)
        answer = await self.llm_service.execute(
            text=new_message,
            history=[(message.role, message.text) for message in history]
        )

        await self.message_service.create_message(chat_id, "human", new_message)
        await self.message_service.create_message(chat_id, "assistant", answer.text)
        await self.tr_service.create_transaction(user_id, "chat", -1 * answer.used_tokens)
        return answer