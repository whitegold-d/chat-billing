from pydantic import BaseModel


class AnswerDTO(BaseModel):
    text: str
    used_tokens: int


class NewMessageResponseDTO(BaseModel):
    text: str
    used_tokens: int

    @classmethod
    def from_answer(cls, answer: AnswerDTO) -> "NewMessageResponseDTO":
        return cls(
            text=answer.text,
            used_tokens=answer.used_tokens
        )