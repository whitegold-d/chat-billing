from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID


@dataclass
class TransactionResponseORM:
    id: UUID
    user_id: str
    transaction_type: Literal["chat", "top_up", "u2u"]
    value: int
    created_at: datetime