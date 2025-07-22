from dataclasses import dataclass
from typing import Literal, List


@dataclass
class MessageDTO:
    role: Literal["user", "system"]
    message: str


@dataclass
class QuestionDTO:
    text: str
    history: List[MessageDTO]