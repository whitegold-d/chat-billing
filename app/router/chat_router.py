from http import HTTPStatus

from fastapi import APIRouter, Body
from starlette.responses import JSONResponse

from app.dependency.auth_dependency import AuthServiceDependency
from app.dependency.llm_dependency import TransactionServiceDependency, LLMServiceDependency, MessageServiceDependency, \
    ManagerServiceDependency, RagServiceDependency
from app.interface.http.model.request.llm_request_dto import TopUpRequestDTO, NewMessageRequestDTO, \
    MoveTransactionRequestDTO
from app.interface.http.model.response.llm_response_dto import NewMessageResponseDTO
from app.interface.http.model.response.message_response_dto import SuccessMessage, ErrorMessage

chat_router = APIRouter(prefix="/chat", tags=["chat"])

@chat_router.post('/users/{user_id}/balance/up', response_model=SuccessMessage)
async def top_up_user_balance(user_id: str,
                              auth_service: AuthServiceDependency,
                              tr_service: TransactionServiceDependency,
                              tokens: TopUpRequestDTO = Body()) -> JSONResponse:
    user = await auth_service.get_user_by_id(user_id)
    if user is None:
        return JSONResponse(content=ErrorMessage(message="User not found").model_dump(),
                            status_code=HTTPStatus.NOT_FOUND)

    transaction_response = await tr_service.create_transaction(
        user_id=user_id,
        transaction_type="top_up",
        value=tokens.value)

    if not transaction_response:
        return JSONResponse(content=ErrorMessage(message="Transaction failed").model_dump(),
                            status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    total_count = await tr_service.get_current_balance(user_id)

    return JSONResponse(content=SuccessMessage(
        message=f"Successfully added {transaction_response.value} tokens. Total count: {total_count}").model_dump(),
        status_code=HTTPStatus.OK)


@chat_router.get('/users/{user_id}/balance', response_model=SuccessMessage)
async def get_balance(user_id: str,
                      transaction_service: TransactionServiceDependency,
                      auth_service: AuthServiceDependency):
    user = await auth_service.get_user_by_id(user_id)
    if user is None:
        return JSONResponse(content=ErrorMessage(message="User not found").model_dump(),
                            status_code=HTTPStatus.NOT_FOUND)

    balance = await transaction_service.get_current_balance(user_id)
    return JSONResponse(content=SuccessMessage(message=f"Current balance: {balance}").model_dump(),
                        status_code=HTTPStatus.OK)


@chat_router.post("/users/{user_id}/chat/{chat_id}", response_model=NewMessageResponseDTO)
async def send_message(user_id: str,
                       chat_id: int,
                       auth_service: AuthServiceDependency,
                       tr_service: TransactionServiceDependency,
                       manager_service: ManagerServiceDependency,
                       new_message: NewMessageRequestDTO = Body()
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


@chat_router.post("/users/donate", response_model=SuccessMessage)
async def donate(auth_service: AuthServiceDependency,
                 tr_service: TransactionServiceDependency,
                 request: MoveTransactionRequestDTO = Body()) -> JSONResponse:
    user_giving = await auth_service.get_user_by_id(request.tokens_giving_user_id)
    user_taking = await auth_service.get_user_by_id(request.tokens_taking_user_id)
    if user_giving is None or user_taking is None:
        return JSONResponse(content=ErrorMessage(message="Donating or receiving user not found").model_dump(),
                            status_code=HTTPStatus.NOT_FOUND)
    if not await tr_service.move_tokens(user_giving.id, user_taking.id, request.value):
        return JSONResponse(content=ErrorMessage(message="Something went wrong").model_dump(),
                            status_code=HTTPStatus.NOT_FOUND)
    return JSONResponse(content=SuccessMessage(message="Tokens were transferred successfully").model_dump(),
                            status_code=HTTPStatus.OK)


@chat_router.post("/users/upload")
async def upload_document(manager_service: ManagerServiceDependency,
                          document_name: str):
    await manager_service.upload_documents("./documents/" + document_name)


@chat_router.post("/users/retrieve")
async def retrieve_information(manager_service: ManagerServiceDependency):
    await manager_service.retrieve_information(user_query="Что такое симметричное биномиальное распределение",
                                               limit=5)