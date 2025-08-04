from abc import ABC, abstractmethod
from typing import List

from app.infrastructure.db.model.request.move_transaction_request import MoveTransactionRequest
from app.infrastructure.db.model.request.transaction_request import TransactionRequestORM
from app.infrastructure.db.model.response.transaction_response import TransactionResponseORM


class BaseTransactionRepository(ABC):
    @abstractmethod
    async def get_all_transactions(self, **filters) -> List[TransactionResponseORM]:
        raise NotImplementedError

    @abstractmethod
    async def create_transaction(self, data: TransactionRequestORM) -> TransactionResponseORM:
        raise NotImplementedError

    @abstractmethod
    async def move_tokens_transaction(self, data: MoveTransactionRequest) -> bool:
        raise NotImplementedError