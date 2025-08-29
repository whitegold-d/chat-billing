from typing import Annotated

from fastapi import Depends

from app.rag.rag import RAG
from app.infrastructure.db.repository.implementation.postgresql_message_repository import PostgreSQLMessageRepository
from app.infrastructure.db.repository.implementation.postgresql_transaction_repository import \
    PostgreSQLTransactionRepository
from app.infrastructure.db.repository.interface.base_message_repository import BaseMessageRepository
from app.infrastructure.db.repository.interface.base_transaction_repository import BaseTransactionRepository
from app.service.implementation.agent_service import AgentService, AgentConfig
from app.service.implementation.chat_session_manager import ChatSessionManager
from app.service.implementation.llama_llm_service import LlamaLLMService
from app.service.implementation.message_service import MessageService
from app.service.implementation.transaction_service import TransactionService
from app.service.interface.base_agent_service import BaseAgentService
from app.service.interface.base_chat_session_manager import BaseChatSessionManager
from app.service.interface.base_llm_service import BaseLLMService
from app.service.interface.base_message_service import BaseMessageService
from app.service.interface.base_transaction_service import BaseTransactionService


def get_transaction_repo() -> BaseTransactionRepository:
    return PostgreSQLTransactionRepository()

def get_transaction_service(repo: BaseTransactionRepository = Depends(get_transaction_repo)) -> BaseTransactionService:
    return TransactionService(repo)

def get_message_repo() -> BaseMessageRepository:
    return PostgreSQLMessageRepository()

def get_message_service(repo: BaseMessageRepository = Depends(get_message_repo)) -> BaseMessageService:
    return MessageService(repo)

def get_agent_service() -> BaseAgentService:
    llm_service = AgentService(
        llm=AgentConfig(
            model_name="qwen3:8b",
            ollama_base_url="http://localhost:11434"),
        llm_vacancy=AgentConfig(
            model_name="qwen3:8b",
            ollama_base_url="http://localhost:11434"),
    )
    return llm_service

def get_rag_model():
    return RAG(db_type='pgvector')

def get_chat_session_manager(message_service = Depends(get_message_service),
                             tr_service = Depends(get_transaction_service),
                             agent_service = Depends(get_agent_service),
                             rag_service = Depends(get_rag_model)) -> BaseChatSessionManager:
    return ChatSessionManager(message_service, tr_service, agent_service, rag_service)


TransactionServiceDependency = Annotated[BaseTransactionService, Depends(get_transaction_service)]
MessageServiceDependency = Annotated[BaseMessageService, Depends(get_message_service)]
LLMServiceDependency = Annotated[BaseLLMService, Depends(get_agent_service)]
ManagerServiceDependency = Annotated[BaseChatSessionManager, Depends(get_chat_session_manager)]
RagServiceDependency = Annotated[RAG, Depends(get_rag_model)]
