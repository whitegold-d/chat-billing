from dataclasses import dataclass
from typing import Literal


@dataclass
class TransactionRequestORM:
    user_id: str
    transaction_type: Literal["chat", "top_up"]
    value: int
