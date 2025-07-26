from typing import Annotated

from fastapi import Depends

from app.infrastructure.db.repository.implementation.in_memory_message_repository import InMemoryMessageRepository
from app.infrastructure.db.repository.implementation.in_memory_transaction_repository import \
    InMemoryTransactionRepository
from app.infrastructure.db.repository.interface.base_message_repository import BaseMessageRepository
from app.infrastructure.db.repository.interface.base_transaction_repository import BaseTransactionRepository
from app.service.implementation.llama_llm_service import LlamaLLMService
from app.service.interface.base_llm_service import BaseLLMService
from app.service.interface.base_message_service import BaseMessageService
from app.service.interface.base_transaction_service import BaseTransactionService


def get_transaction_repo() -> BaseTransactionRepository:
    return InMemoryTransactionRepository()

def get_transaction_service(service: BaseTransactionService = Depends(get_transaction_repo)) -> BaseTransactionService:
    return service

def get_message_repo() -> BaseMessageRepository:
    return InMemoryMessageRepository()

def get_message_service(service: BaseMessageService = Depends(get_message_repo)) -> BaseMessageService:
    return service

def get_llm_service() -> BaseLLMService:
    llm_service = LlamaLLMService(
        model_name="deepseek-r1:8b",
        ollama_base_url="http://localhost:11434"
    )
    return llm_service

TransactionServiceDependency = Annotated[BaseTransactionService, get_transaction_service()]
MessageServiceDependency = Annotated[BaseMessageService, get_message_service()]
LLMServiceDependency = Annotated[BaseLLMService, get_llm_service()]
