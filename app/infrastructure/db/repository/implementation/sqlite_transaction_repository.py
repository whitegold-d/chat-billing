import datetime
from typing import List
from uuid import uuid4

from fastapi import HTTPException

from app.infrastructure.db.model.request.transaction_request import TransactionRequestORM
from app.infrastructure.db.model.response.transaction_response import TransactionResponseORM
from app.infrastructure.db.repository.interface.base_transaction_repository import BaseTransactionRepository

import sqlite3

from app.utils.constants import DB_PATH


class SQLiteTransactionRepository(BaseTransactionRepository):
    _self = None

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    async def get_all_transactions(self, **filters) -> List[TransactionResponseORM] | None:
        result = []

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM transaction_model""")
            transaction_tuples = cursor.fetchall()

        if not transaction_tuples:
            return None

        transactions = [TransactionResponseORM(*transaction) for transaction in transaction_tuples]
        for key, value in filters.items():
            for transaction in transactions:
                if hasattr(transaction, key):
                    actual_value = getattr(transaction, key)
                    if actual_value == value:
                        result.append(transaction)

        return result


    async def create_transaction(self, data: TransactionRequestORM) -> TransactionResponseORM | None:
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                transaction_id = uuid4()
                date = datetime.datetime.now()
                cursor.execute(
                    """INSERT INTO transaction_model (id, user_id, transaction_type, value, created_at) VALUES (?, ?, ?, ?, ?)""",
                    (str(transaction_id),
                     data.user_id,
                     data.transaction_type,
                     data.value,
                     str(date)
                     ))
                conn.commit()
            return TransactionResponseORM(transaction_id, data.user_id, data.transaction_type, data.value, date)
        except sqlite3.Error as error:
            if conn:
                conn.rollback()
            return None
        finally:
            conn.close()