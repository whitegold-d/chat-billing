from abc import ABC, abstractmethod
from typing import Literal

from app.infrastructure.db.model.response.transaction_response import TransactionResponseORM


class BaseTransactionService(ABC):
    @abstractmethod
    async def create_transaction(self, user_id: str,
                                 transaction_type: Literal["chat", "top_up"],
                                 value: int) -> TransactionResponseORM:
        raise NotImplementedError()

    @abstractmethod
    async def get_current_balance(self, user_id: str) -> int:
        raise NotImplementedError()


    @abstractmethod
    async def move_tokens(self, token_giving_user_id: str, token_taking_user_id: str, value: int) -> bool:
        raise NotImplementedError()