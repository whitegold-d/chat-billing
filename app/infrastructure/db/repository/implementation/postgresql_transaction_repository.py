from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from app.infrastructure.db.model.request.transaction_request import TransactionRequestORM
from app.infrastructure.db.model.request.user_request import UserRequestORM
from app.infrastructure.db.model.response.transaction_response import TransactionResponseORM
from app.infrastructure.db.model.response.user_response import UserResponseORM
from app.infrastructure.db.repository.interface.base_transaction_repository import BaseTransactionRepository
from app.infrastructure.db.repository.interface.base_user_repository import BaseUserRepository
from app.utils.constants import PG_DATABASE_DSN


class PostgreSQLTransactionRepository(BaseTransactionRepository):
    dsn = PG_DATABASE_DSN
    _self = None

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    async def get_all_transactions(self, **filters) -> List[TransactionResponseORM] | None:
        async with self._get_db_connection() as connection:
            await connection.execute("""SELECT * from transaction_model""")
            transactions = await connection.fetch()

        if not transactions:
            return None

        result = []
        for key, value in filters.items():
            for transaction in transactions:
                if transactions.get(key) == value:
                    result.append(transaction)
        return result


    async def create_transaction(self, data: TransactionRequestORM) -> TransactionResponseORM:
        async with self._get_db_connection() as connection:
            transaction_id = uuid4()
            date_now = datetime.now()
            await connection.execute("""INSERT INTO transaction_model (id, user_id, transaction_type, value, created_at) VALUES ($1, $2, $3, $4, $5)""",
                               transaction_id, data.user_id, data.transaction_type, data.value, date_now)
        return TransactionResponseORM(transaction_id, data.user_id, data.transaction_type, data.value, date_now)

