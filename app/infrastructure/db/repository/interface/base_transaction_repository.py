from abc import ABC, abstractmethod
from typing import List

from app.infrastructure.db.model.request.transaction_request import TransactionRequestORM
from app.infrastructure.db.model.response.transaction_response import TransactionResponseORM
from app.infrastructure.db.repository.base_repository import BaseRepository


class BaseTransactionRepository(ABC, BaseRepository):
    @abstractmethod
    async def get_all_transactions(self, **filters) -> List[TransactionResponseORM]:
        raise NotImplementedError

    @abstractmethod
    async def create_transaction(self, data: TransactionRequestORM) -> TransactionResponseORM:
        raise NotImplementedError