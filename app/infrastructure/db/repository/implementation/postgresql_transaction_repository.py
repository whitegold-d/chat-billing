from datetime import datetime
from typing import List
from uuid import uuid4, UUID

from sqlalchemy import select, insert

from app.infrastructure.db.model.ORM.transaction_orm import TransactionORM
from app.infrastructure.db.model.ORM.user_orm import UserORM
from app.infrastructure.db.model.request.move_transaction_request import MoveTransactionRequest
from app.infrastructure.db.model.request.transaction_request import TransactionRequestORM
from app.infrastructure.db.model.response.transaction_response import TransactionResponseORM, TransactionType
from app.infrastructure.db.postgresql_connection_manager import PostgreSQLConnectionManager
from app.infrastructure.db.repository.interface.base_transaction_repository import BaseTransactionRepository


class PostgreSQLTransactionRepository(BaseTransactionRepository):
    _self = None

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    async def get_all_transactions(self) -> List[TransactionResponseORM] | None:
        async with PostgreSQLConnectionManager.get_session() as session:
            stmt = select(TransactionORM)
            result = await session.execute(stmt)
            transactions = result.all()
        result = [TransactionResponseORM(*args) for args in transactions]
        return result


    async def create_transaction(self, data: TransactionRequestORM) -> TransactionResponseORM:
        async with PostgreSQLConnectionManager.get_session() as session:
            transaction_id = uuid4()
            date_now = datetime.now()

            stmt = insert(TransactionORM).values(id=transaction_id,
                                                 user_id=data.user_id,
                                                 transaction_type=data.transaction_type,
                                                 value=data.value,
                                                 created_at=date_now)
            await session.execute(stmt)
        return TransactionResponseORM(transaction_id,
                                      UUID(data.user_id),
                                      TransactionType(data.transaction_type),
                                      data.value,
                                      date_now)


    async def move_tokens_transaction(self, data: MoveTransactionRequest) -> bool:
        async with PostgreSQLConnectionManager.get_session() as session:
            async with session.begin():
                await session.execute(insert(TransactionORM).values(user_id=data.token_taking_user_id,
                                                     transaction_type=TransactionType.U2U,
                                                     value=-data.value))
                await session.execute(insert(TransactionORM).values(user_id=data.token_giving_user_id,
                                                     transaction_type=TransactionType.U2U,
                                                     value=data.value))
        return True

