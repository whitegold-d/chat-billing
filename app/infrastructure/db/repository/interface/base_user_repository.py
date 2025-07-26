from abc import ABC, abstractmethod
from typing import List, Optional

from app.infrastructure.db.model.request.user_request import UserRequestORM
from app.infrastructure.db.model.response.user_response import UserResponseORM


class BaseUserRepository(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> Optional[UserResponseORM]:
        raise NotImplementedError


    @abstractmethod
    async def get_all_users(self, **filters) -> List[UserResponseORM]:
        raise NotImplementedError


    @abstractmethod
    async def save_user(self, user: UserRequestORM) -> UserResponseORM:
        raise NotImplementedError
