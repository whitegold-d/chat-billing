from dataclasses import dataclass
from typing import Literal, List, Tuple

from pydantic import BaseModel

HistoryType = List[Tuple[Literal["assistant", "human"], str]]

class NewMessageRequest(BaseModel):
    text: str


class TopUpRequest(BaseModel):
    value: int

