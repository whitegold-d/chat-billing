from typing import List, Optional
from uuid import uuid4

from app.infrastructure.db.model.request.user_request import UserRequestORM
from app.infrastructure.db.model.response.user_response import UserResponseORM
from app.infrastructure.db.postgresql_connection_manager import PostgreSQLConnectionManager
from app.infrastructure.db.repository.interface.base_user_repository import BaseUserRepository
from app.utils.constants import PG_DATABASE_DSN


class PostgreSQLUserRepository(BaseUserRepository):
    dsn = PG_DATABASE_DSN
    _self = None

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    async def get_user_by_id(self, user_id: str) -> Optional[UserResponseORM]:
        async with PostgreSQLConnectionManager.get_connection() as connection:
            users = await connection.fetch("SELECT * FROM users WHERE id = $1", user_id)
        user = users[0] if users else None
        if user is None:
            return None
        return UserResponseORM(id=user["id"], login=user["login"], name=user["name"], hashed_password=user["hashed_password"])

    async def get_all_users(self, **filters) -> List[UserResponseORM] | None:
        async with PostgreSQLConnectionManager.get_connection() as connection:
            users = await connection.fetch("SELECT * from users")

        if not users:
            return None

        result = []
        for key, value in filters.items():
            for user in users:
                if user.get(key) == value:
                    result.append(UserResponseORM(user["id"],
                                                  user["login"],
                                                  user["name"],
                                                  user["hashed_password"]))
        return result

    async def save_user(self, user: UserRequestORM) -> UserResponseORM:
        async with PostgreSQLConnectionManager.get_connection() as connection:
            user_id = uuid4()
            await connection.execute(
                "INSERT INTO users (id, login, name, hashed_password) VALUES ($1, $2, $3, $4)",
                str(user_id), user.login, user.name, user.hashed_password)
        return UserResponseORM(user_id, user.login, user.name, user.hashed_password)