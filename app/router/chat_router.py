from http import HTTPStatus

from fastapi import APIRouter, Body
from starlette.responses import JSONResponse

from app.dependency.auth_dependency import AuthServiceDependency
from app.dependency.llm_dependency import TransactionServiceDependency, LLMServiceDependency, MessageServiceDependency, \
    ManagerServiceDependency
from app.infrastructure.db.repository.implementation.in_memory_message_repository import InMemoryMessageRepository
from app.interface.http.model.request.llm_request_dto import TopUpRequest, NewMessageRequest
from app.interface.http.model.response.llm_response_dto import NewMessageResponseDTO
from app.interface.http.model.response.message_response_dto import SuccessMessage, ErrorMessage

chat_router = APIRouter(prefix="/chat", tags=["chat"])

@chat_router.post('/users/{user_id}/balance/up', response_model=SuccessMessage)
async def top_up_user_balance(user_id: str,
                              auth_service: AuthServiceDependency,
                              tr_service: TransactionServiceDependency,
                              tokens: TopUpRequest = Body()) -> JSONResponse:
    user = await auth_service.get_user_by_id(user_id)
    if user is None:
        return JSONResponse(content=ErrorMessage(message="User not found").model_dump(),
                            status_code=HTTPStatus.NOT_FOUND)

    transaction_response = await tr_service.create_transaction(
        user_id=user_id,
        transaction_type="top_up",
        value=tokens.value)

    total_count = await tr_service.get_current_balance(user_id)

    return JSONResponse(content=SuccessMessage(
        message=f"Successfully added {transaction_response.value} tokens. Total count: {total_count}").model_dump(),
        status_code=HTTPStatus.OK)


@chat_router.post("/users/{user_id}/chat/{chat_id}", response_model=NewMessageResponseDTO)
async def send_message(user_id: str,
                       chat_id: int,
                       auth_service: AuthServiceDependency,
                       tr_service: TransactionServiceDependency,
                       manager_service: ManagerServiceDependency,
                       new_message: NewMessageRequest = Body()
                     ) -> JSONResponse:
    user = await auth_service.get_user_by_id(user_id)
    if user is None:
        return JSONResponse(content=ErrorMessage(message="User not found").model_dump(),
                            status_code=HTTPStatus.NOT_FOUND)
    cur_balance = await tr_service.get_current_balance(user_id)
    if cur_balance <= 0:
        return JSONResponse(content=ErrorMessage(message=f"Current balance is {cur_balance}, you need to top up your balance").model_dump(),
                            status_code=HTTPStatus.NOT_FOUND)
    answer = await manager_service.send_message(chat_id, user_id, new_message.text)
    return JSONResponse(content=NewMessageResponseDTO.from_answer(answer).model_dump())
