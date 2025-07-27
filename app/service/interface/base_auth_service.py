from abc import ABC, abstractmethod
from typing import Optional

from app.infrastructure.db.model.response.user_response import UserResponseORM


class BaseAuthService(ABC):
    @abstractmethod
    async def login(self, login: str, password: str) -> Optional[UserResponseORM]:
        raise NotImplementedError()

    @abstractmethod
    async def register(self, login: str, name: str, password: str) -> UserResponseORM:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> Optional[UserResponseORM]:
        raise NotImplementedError()