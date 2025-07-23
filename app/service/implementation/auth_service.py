from typing import Optional

import bcrypt
from passlib.context import CryptContext

from app.infrastructure.db.model.request.user_request import UserRequest
from app.infrastructure.db.model.response.user_response import UserResponse
from app.infrastructure.db.repository.interface.user_repository import UserRepository
from app.service.interface.base_auth_service import BaseAuthService


class AuthService(BaseAuthService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository


    async def login(self, login: str, password: str) -> Optional[UserResponse]:
        users = await self.user_repository.get_all_users(login=login)
        for user in users:
            if self._verify_password(password=password, hashed_password=user.hashed_password):
                return user
        return None


    async def register(self, login: str, name: str, password: str) -> UserResponse:
        hashed_password = self._hash_password(password=password)
        user_response = await self.user_repository.save_user(UserRequest(login=login,
                                                   name=name,
                                                   hashed_password=hashed_password))
        return user_response


    async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        user = await self.user_repository.get_user_by_id(user_id=user_id)
        return user


    @staticmethod
    def _hash_password(password: str) -> str:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)


    @staticmethod
    def _verify_password(password: str, hashed_password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        check = pwd_context.verify(password, hashed_password)
        return check