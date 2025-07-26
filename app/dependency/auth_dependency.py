from typing import Annotated, Optional

from fastapi import Depends, Header

from app.infrastructure.db.repository.implementation.in_memory_user_repository import InMemoryUserRepository
from app.infrastructure.db.repository.interface.base_user_repository import BaseUserRepository
from app.interface.http.model.response.auth_response_dto import UserResponseSchemaDTO
from app.service.implementation.auth_service import AuthService
from app.service.interface.base_auth_service import BaseAuthService


def get_repo():
    return InMemoryUserRepository()

def get_auth_service(auth_repo: BaseUserRepository = Depends(get_repo)):
    return AuthService(auth_repo)

async def get_current_user(
        user_id: Optional[str] = Header(alias='X-User-Id', default=None),
        auth_service: AuthService = Depends(get_auth_service)) -> Optional[UserResponseSchemaDTO]:
    if not user_id:
        return None
    user = await auth_service.get_user_by_id(user_id)
    if not user:
        return None
    user_dto = UserResponseSchemaDTO.from_orm(user)
    return user_dto


AuthServiceDependency = Annotated[BaseAuthService, Depends(get_auth_service)]
CurrentUserDependency = Annotated[UserResponseSchemaDTO, Depends(get_current_user)]
