from abc import ABC, abstractmethod

from app.interface.http.model.request.llm_request_dto import HistoryType
from app.interface.http.model.response.llm_response_dto import AnswerDTO


class BaseLLMService(ABC):
    @abstractmethod
    async def execute(self, text: str, history: HistoryType) -> AnswerDTO:
        raise NotImplementedError()