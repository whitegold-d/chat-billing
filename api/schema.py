from abc import ABC, abstractmethod
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


@dataclass
class AnswerDTO:
    text: str
    used_tokens: int


class LLMService(ABC):
    @abstractmethod
    async def execute(self, data: QuestionDTO) -> AnswerDTO:
        raise NotImplementedError()