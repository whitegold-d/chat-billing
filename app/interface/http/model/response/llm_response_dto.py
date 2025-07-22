from dataclasses import dataclass


@dataclass
class AnswerDTO:
    text: str
    used_tokens: int