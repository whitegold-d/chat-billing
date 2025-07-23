import asyncio

from app.interface.http.model.request.llm_request_dto import QuestionDTO
from app.service.implementation.llama_llm_service import LlamaLLMService


async def main():
    llm_service = LlamaLLMService(
        model_name="deepseek-r1:8b",
        ollama_base_url="http://localhost:11434")
    answer = await llm_service.execute(QuestionDTO(text="Hi, how are you?", history=[]))
    print(answer.text)
    print(answer.used_tokens)

if __name__ == '__main__':
    asyncio.run(main())