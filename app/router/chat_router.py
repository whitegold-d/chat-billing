from http import HTTPStatus

from fastapi import APIRouter, Body
from starlette.responses import JSONResponse

from app.dependency.auth_dependency import AuthServiceDependency
from app.dependency.llm_dependency import TransactionServiceDependency
from app.interface.http.model.request.llm_request_dto import TopUpRequest
from app.interface.http.model.response.message_response_dto import SuccessMessage, ErrorMessage

chat_router = APIRouter(prefix="/chat", tags=["chat"])

@chat_router.post('/users/{user_id}/balance/up', response_model=SuccessMessage)
async def top_up_user_balance(user_id: str,
                              auth_service: AuthServiceDependency,
                              tr_service: TransactionServiceDependency,
                              tokens: TopUpRequest = Body()) -> JSONResponse:
    user = auth_service.get_user_by_id(user_id)
    if user is None:
        return JSONResponse(content=ErrorMessage(message="User not found"), status_code=HTTPStatus.NOT_FOUND)

    transaction_response = await tr_service.create_transaction(
        user_id,
        transaction_service="top_up",
        value=tokens.value)

    total_count = tr_service.get_current_balance(user_id)

    return JSONResponse(content=SuccessMessage(
        message=f"Successfully added {transaction_response.value} tokens. Total count: {total_count}"),
        status_code=HTTPStatus.OK)