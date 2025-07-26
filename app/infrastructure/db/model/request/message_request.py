from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass
class MessageRequestORM:
    chat_id: str
    role: Literal["assistant", "human"]
    text: str