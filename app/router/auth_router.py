from typing import Annotated

from fastapi import APIRouter, Depends, Body
from starlette import status
from starlette.responses import JSONResponse

from app.dependency.auth_dependency import get_auth_service, AuthServiceDependency
from app.interface.http.model.request.auth_request_dto import RegisterRequestDTO
from app.interface.http.model.response.message_response_dto import SuccessMessage
from app.service.implementation.auth_service import AuthService
from app.service.interface.base_auth_service import BaseAuthService

router = APIRouter(prefix='/auth', tags=["authorization"])

@router.get('/register')
async def register(service: AuthService = AuthServiceDependency,
                   data: RegisterRequestDTO = Body()) -> JSONResponse:
    user_response = await service.register(
        data.login,
        data.name,
        data.password)
    return JSONResponse(
        content=SuccessMessage(message=f"User {user_response.name} has been successfully registered").model_dump(),
        status_code=status.HTTP_201_CREATED)

