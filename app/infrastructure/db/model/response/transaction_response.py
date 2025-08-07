from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Literal
from uuid import UUID


class TransactionType(StrEnum):
    U2U = "u2u"
    TOP_UP = "top_up"
    CHAT = "chat"


@dataclass
class TransactionResponseORM:
    id: UUID
    user_id: UUID
    transaction_type: TransactionType
    value: int
    created_at: datetime