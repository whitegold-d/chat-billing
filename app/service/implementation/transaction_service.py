from typing import Literal

from app.infrastructure.db.model.request.transaction_request import TransactionRequestORM
from app.infrastructure.db.repository.interface.base_transaction_repository import BaseTransactionRepository
from app.service.interface.base_transaction_service import BaseTransactionService


class TransactionService(BaseTransactionService):
    _self = None

    def __new__(cls, transaction_repository: BaseTransactionRepository):
        if not cls._self:
            cls._self = super().__new__(cls)
            cls._self.transaction_repository = transaction_repository
        return cls._self


    async def create_transaction(self, user_id: str,
                                 transaction_type: Literal["chat", "top_up"],
                                 value: int):
        new_transaction = await self.transaction_repository.create_transaction(
            TransactionRequestORM(
                user_id = user_id,
                transaction_type = transaction_type,
                value = value
            ))
        return new_transaction


    async def get_current_balance(self, user_id: str):
        transactions = await self.transaction_repository.get_all_transactions(user_id=user_id)
        result_value = sum(tr.value for tr in transactions)
        return result_value