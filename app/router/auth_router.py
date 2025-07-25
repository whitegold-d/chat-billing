from fastapi import APIRouter, Body
from starlette import status
from starlette.responses import JSONResponse

from app.dependency.auth_dependency import AuthServiceDependency, CurrentUserDependency
from app.interface.http.model.request.auth_request_dto import RegisterRequestDTO, LoginRequestDTO
from app.interface.http.model.response.auth_response_dto import LoginResponseDTO, UserResponseSchemaDTO
from app.interface.http.model.response.message_response_dto import SuccessMessage, ErrorMessage
from app.service.implementation.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=["authorization"])

@router.post('/register', response_model=SuccessMessage)
async def register(service: AuthServiceDependency,
                   data: RegisterRequestDTO = Body()) -> JSONResponse:
    user_response = await service.register(
        data.login,
        data.name,
        data.password)
    return JSONResponse(
        content=SuccessMessage(message=f"User {user_response.name} has been successfully registered, id: {user_response.id}").model_dump(),
        status_code=status.HTTP_201_CREATED)


@router.post('/login', response_model=LoginResponseDTO)
async def login(service: AuthServiceDependency,
                   data: LoginRequestDTO = Body()) -> JSONResponse:
    user_response = await service.login(
        data.login,
        data.password)
    if not user_response:
        return JSONResponse(
            content=ErrorMessage(message=f"User {data.login} was not found").model_dump(),
            status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(
        content=LoginResponseDTO.from_orm(user_response).model_dump(),
        status_code=status.HTTP_200_OK)


@router.get('/get_user', response_model=UserResponseSchemaDTO)
async def get_cur_user(user: CurrentUserDependency) -> JSONResponse:
    if not user:
        return JSONResponse(
            content=ErrorMessage(message=f"Current user was not found").model_dump(),
            status_code=status.HTTP_401_UNAUTHORIZED)

    return JSONResponse(
        content=UserResponseSchemaDTO.from_orm(user).model_dump(),
        status_code=status.HTTP_200_OK)
