from abc import ABC, abstractmethod

from app.interface.http.model.request.llm_request_dto import QuestionDTO
from app.interface.http.model.response.llm_response_dto import AnswerDTO


class LLMService(ABC):
    @abstractmethod
    async def execute(self, data: QuestionDTO) -> AnswerDTO:
        raise NotImplementedError()