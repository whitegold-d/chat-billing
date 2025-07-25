from pydantic import BaseModel


class SuccessMessage(BaseModel):
    message: str


class ErrorMessage(BaseModel):
    message: str