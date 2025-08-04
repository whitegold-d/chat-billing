from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from app.infrastructure.db.model.request.move_transaction_request import MoveTransactionRequest
from app.infrastructure.db.model.request.transaction_request import TransactionRequestORM
from app.infrastructure.db.model.request.user_request import UserRequestORM
from app.infrastructure.db.model.response.transaction_response import TransactionResponseORM
from app.infrastructure.db.model.response.user_response import UserResponseORM
from app.infrastructure.db.postgresql_connection_manager import PostgreSQLConnectionManager
from app.infrastructure.db.repository.interface.base_transaction_repository import BaseTransactionRepository
from app.infrastructure.db.repository.interface.base_user_repository import BaseUserRepository
from app.utils.constants import PG_DATABASE_DSN


class PostgreSQLTransactionRepository(BaseTransactionRepository):
    _self = None

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    async def get_all_transactions(self, **filters) -> List[TransactionResponseORM] | None:
        async with PostgreSQLConnectionManager.get_connection() as connection:
            transactions = await connection.fetch("SELECT * from transaction_model")

        if not transactions:
            return None

        result = []
        for key, value in filters.items():
            for transaction in transactions:
                if transaction.get(key) == value:
                    result.append(transaction)
        return result


    async def create_transaction(self, data: TransactionRequestORM) -> TransactionResponseORM:
        async with PostgreSQLConnectionManager.get_connection() as connection:
            transaction_id = uuid4()
            date_now = datetime.now()
            await connection.execute("INSERT INTO transaction_model (id, user_id, transaction_type, value, created_at) VALUES ($1, $2, $3, $4, $5)",
                               str(transaction_id), data.user_id, data.transaction_type, data.value, date_now)
        return TransactionResponseORM(transaction_id, data.user_id, data.transaction_type, data.value, date_now)


    async def move_tokens_transaction(self, data: MoveTransactionRequest) -> bool:
        try:
            async with PostgreSQLConnectionManager.get_connection() as connection:
                id_1 = str(uuid4())
                id_2 = str(uuid4())
                async with connection.transaction():
                    await connection.execute("""
                        INSERT INTO transaction_model (id, user_id, transaction_type, value, created_at) 
                        VALUES ($1, $2, $3, $4, $5)""", id_1, data.token_giving_user_id, "u2u", -data.value, datetime.now())
                    await connection.execute("""
                        INSERT INTO transaction_model (id, user_id, transaction_type, value, created_at) 
                        VALUES ($1, $2, $3, $4, $5)""", id_2, data.token_taking_user_id, "u2u", data.value, datetime.now())
        except Exception as e:
            return False
        return True

