from pydantic import BaseModel, Field

from app.interface.http.model.response.llm_response_dto import AnswerDTO


class RegisterRequestDTO(BaseModel):
    login: str
    name: str
    password: str


class LoginRequestDTO(BaseModel):
    login: str
    password: str