from typing import List, Optional

from app.infrastructure.db.model.request.user_request import UserRequestORM
from app.infrastructure.db.model.response.user_response import UserResponseORM

from uuid import UUID, uuid4
from app.infrastructure.db.repository.interface.base_user_repository import BaseUserRepository


class InMemoryUserRepository(BaseUserRepository):
    users: List[UserResponseORM] = []
    _self = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    async def get_user_by_id(self, user_id: str) -> Optional[UserResponseORM]:
        for user in self.users:
            if str(user.id) == user_id:
                return user
        return None


    async def get_all_users(self, **filters) -> List[UserResponseORM]:
        result = []
        if filters:
            for key, value in filters.items():
                for user in self.users:
                    if hasattr(user, key):
                        actual_value = getattr(user, key)
                        if actual_value == value:
                            result.append(user)
            return result
        return self.users


    async def save_user(self, new_user: UserRequestORM) -> UserResponseORM:
        user = UserResponseORM(
            id = uuid4(),
            name=new_user.name,
            login=new_user.login,
            hashed_password=new_user.hashed_password)
        self.users.append(user)
        return user