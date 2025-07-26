from datetime import datetime
from typing import List
from uuid import uuid4

from app.infrastructure.db.model.request.transaction_request import TransactionRequestORM
from app.infrastructure.db.model.response.transaction_response import TransactionResponseORM
from app.infrastructure.db.repository.interface.base_transaction_repository import BaseTransactionRepository


class InMemoryTransactionRepository(BaseTransactionRepository):
    _self = None
    transactions: List[TransactionResponseORM] = []

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            cls._self = object.__new__(cls)
        return cls._self


    async def create_transaction(self, data: TransactionRequestORM) -> TransactionResponseORM:
        new_transaction = TransactionResponseORM(
            id = uuid4(),
            user_id = data.user_id,
            transaction_type=data.transaction_type,
            value=data.value,
            created_at=datetime.now()
        )
        self.transactions.append(new_transaction)
        return new_transaction


    async def get_all_transactions(self, **filters) -> List[TransactionResponseORM]:
        if filters is None:
            return self.transactions

        result_transaction = []
        for key, value in filters.items():
            for transaction in self.transactions:
                if hasattr(transaction, key):
                    if getattr(transaction, key) == value:
                        result_transaction.append(transaction)
        return result_transaction