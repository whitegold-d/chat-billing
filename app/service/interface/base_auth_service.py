from abc import ABC, abstractmethod
from typing import Optional

from app.infrastructure.db.model.response.user_response import UserResponse


class BaseAuthService(ABC):
    @abstractmethod
    def login(self, login: str, password: str) -> Optional[UserResponse]:
        raise NotImplementedError()

    @abstractmethod
    def register(self, login: str, name: str, password: str) -> UserResponse:
        raise NotImplementedError()

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        raise NotImplementedError()