from dataclasses import dataclass
from typing import Literal, List, Tuple

from pydantic import BaseModel

HistoryType = List[Tuple[Literal["assistant", "human"], str]]

class NewMessageRequestDTO(BaseModel):
    text: str


class TopUpRequestDTO(BaseModel):
    value: int


class MoveTransactionRequestDTO(BaseModel):
    tokens_giving_user_id: str
    tokens_taking_user_id: str
    value: int



