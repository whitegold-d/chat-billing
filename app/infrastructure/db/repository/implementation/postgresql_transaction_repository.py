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
            transactions = result.scalars().all()
        result = [TransactionResponseORM(transaction.id,
                                         transaction.user_id,
                                         transaction.transaction_type,
                                         transaction.value,
                                         transaction.created_at) for transaction in transactions]
        return result


    async def create_transaction(self, data: TransactionRequestORM) -> TransactionResponseORM:
        async with PostgreSQLConnectionManager.get_session() as session:
            transaction_id = uuid4()
            date_now = datetime.now()

            print(f"id: {transaction_id}, data.user_id: {data.user_id}, data.transaction_type: {data.transaction_type}, data.value: {data.value}, date_now: {date_now}")

            stmt = insert(TransactionORM).values(id=transaction_id,
                                                 user_id=data.user_id,
                                                 transaction_type=data.transaction_type,
                                                 value=data.value,
                                                 created_at=date_now)
            await session.execute(stmt)
            await session.commit()
        return TransactionResponseORM(transaction_id,
                                      UUID(data.user_id),
                                      TransactionType(data.transaction_type),
                                      data.value,
                                      date_now)


    async def move_tokens_transaction(self, data: MoveTransactionRequest) -> bool:
        async with PostgreSQLConnectionManager.get_session() as session:
            async with session.begin():
                await session.execute(insert(TransactionORM).values(user_id=data.token_giving_user_id,
                                                     transaction_type=TransactionType.U2U,
                                                     value=-data.value))
                await session.execute(insert(TransactionORM).values(user_id=data.token_taking_user_id,
                                                     transaction_type=TransactionType.U2U,
                                                     value=data.value))
        return True


    async def get_transactions_by_user_id(self, user_id: str) -> List[TransactionResponseORM]:
        async with PostgreSQLConnectionManager.get_session() as session:
            stmt = select(TransactionORM).where(TransactionORM.user_id == UUID(str(user_id)))
            result = await session.execute(stmt)
            transactions = result.scalars().all()
        result = [TransactionResponseORM(transaction.id,
                                         transaction.user_id,
                                         transaction.transaction_type,
                                         transaction.value,
                                         transaction.created_at) for transaction in transactions]
        return result

