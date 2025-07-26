from typing import Optional

import bcrypt
from passlib.context import CryptContext

from app.infrastructure.db.model.request.user_request import UserRequestORM
from app.infrastructure.db.model.response.user_response import UserResponseORM
from app.infrastructure.db.repository.interface.base_user_repository import BaseUserRepository
from app.service.interface.base_auth_service import BaseAuthService


class AuthService(BaseAuthService):
    _self = None

    def __new__(cls, user_repository: BaseUserRepository):
        if cls._self is None:
            cls._self = super().__new__(cls)
            cls._self.user_repository = user_repository
        return cls._self


    async def login(self, login: str, password: str) -> Optional[UserResponseORM]:
        users = await self.user_repository.get_all_users(login=login)
        for user in users:
            if self._verify_password(password=password, hashed_password=user.hashed_password):
                return user
        return None


    async def register(self, login: str, name: str, password: str) -> UserResponseORM:
        hashed_password = self._hash_password(password=password)
        user_response = await self.user_repository.save_user(UserRequestORM(login=login,
                                                                            name=name,
                                                                            hashed_password=hashed_password))
        return user_response


    async def get_user_by_id(self, user_id: str) -> Optional[UserResponseORM]:
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