from contextlib import asynccontextmanager
from http import HTTPStatus
from urllib.request import Request

from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.dependency.db_dependency import current_db
from app.rag.rag import RAG
from app.interface.http.model.response.message_response_dto import ErrorMessage
from app.router.auth_router import auth_router
from app.router.chat_router import chat_router
from app.utils.settings import Settings

from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor


@asynccontextmanager
async def lifespan(app: FastAPI):
    RAG()
    await current_db.initialize_db()
    yield

settings = Settings()
app = FastAPI(title="billing-app", description="", version="1.0", lifespan=lifespan)
app.include_router(router=auth_router, prefix="/api/v1")
app.include_router(router=chat_router, prefix="/api/v1")

tracer_provider = register(
  project_name="chat-billing",
  endpoint="http://localhost:6006/v1/traces",
)
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

@app.exception_handler(500)
async def exception_handler(request: Request, ex: Exception) -> JSONResponse:
    return JSONResponse(content=ErrorMessage(message=f"An error occurred: {ex}"),
                        status_code=HTTPStatus.INTERNAL_SERVER_ERROR)