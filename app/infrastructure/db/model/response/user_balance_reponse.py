from dataclasses import dataclass
from typing import List
from uuid import UUID

from app.infrastructure.db.model.ORM.transaction_orm import TransactionORM


@dataclass
class UserBalanceResponseORM:
    id: UUID
    login: str
    name: str
    balance: float
    transactions: List[TransactionORM]