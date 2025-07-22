from abc import ABC, abstractmethod
from typing import List, Optional

from app.infrastructure.db.model.request.user_request import UserRequest
from app.infrastructure.db.model.response.user_response import UserResponse


class UserRepository(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        raise NotImplementedError


    @abstractmethod
    async def get_all_users(self) -> List[UserResponse]:
        raise NotImplementedError


    @abstractmethod
    async def save_user(self, user: UserRequest) -> UserResponse:
        raise NotImplementedError
