from typing import Annotated

from fastapi import Depends

from app.infrastructure.db.repository.implementation.in_memory_user_repository import InMemoryUserRepository
from app.infrastructure.db.repository.interface.user_repository import UserRepository
from app.service.implementation.auth_service import AuthService
from app.service.interface.base_auth_service import BaseAuthService


def get_repo():
    return InMemoryUserRepository()

def get_auth_service():
    auth_service = AuthService(user_repository = Depends(get_repo))
    return auth_service

AuthServiceDependency = Annotated[BaseAuthService, Depends(get_auth_service)]
