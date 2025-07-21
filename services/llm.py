from typing import cast

from langchain_core.messages import AIMessage
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_openai import ChatOpenAI

from api.schema import AnswerDTO, LLMService, QuestionDTO


class CustomLLMService(LLMService):
    _MESSAGES = [("system", "You are friendly agent"),
                 MessagesPlaceholder("history"),
                 ("user", "{question}")]

    def __init__(self, model_name: str, ollama_base_url: str):
        llm = ChatOpenAI(model=model_name,
                         base_url=f"{ollama_base_url}/v1")
        prompt = ChatPromptTemplate.from_messages(self._MESSAGES)
        self.chain = prompt | llm

    async def execute(self, data: QuestionDTO) -> AnswerDTO:
        answer = await self.chain.ainvoke(
            {"question": data.text,
             "history": [(message.role, message.message) for message in data.history]})
        answer = cast(AIMessage, answer)
        result = AnswerDTO(
            text=answer.content,
            used_tokens=answer.usage_metadata.get("total_tokens", 0))
        return result
