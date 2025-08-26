from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID


@dataclass
class MessageResponseORM:
    id: UUID
    chat_id: str
    role: Literal["assistant", "human", "tool"]
    text: str
    created_at: datetime