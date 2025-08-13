from typing import List, Optional
from uuid import uuid4

from sqlalchemy import select, insert

from app.infrastructure.db.model.ORM.user_orm import UserORM
from app.infrastructure.db.model.request.user_request import UserRequestORM
from app.infrastructure.db.model.response.user_response import UserResponseORM
from app.infrastructure.db.postgresql_connection_manager import PostgreSQLConnectionManager
from app.infrastructure.db.repository.interface.base_user_repository import BaseUserRepository


class PostgreSQLUserRepository(BaseUserRepository):
    _self = None

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self


    async def get_user_by_id(self, user_id: str) -> Optional[UserResponseORM]:
        async with PostgreSQLConnectionManager.get_session() as session:
            stmt = select(UserORM).where(UserORM.id == user_id)
            result = await session.excecute(stmt)
            user = result.scalar_one_or_none()

        if not user:
            return None
        return UserResponseORM(user.id, user.login, user.name, user.hashed_password)


    async def get_all_users(self) -> List[UserResponseORM] | None:
        async with PostgreSQLConnectionManager.get_session() as session:
            stmt = select(UserORM)
            result = await session.execute(stmt)
            users = result.all()

        result = [UserResponseORM(*args) for args in users]
        return result


    async def save_user(self, user: UserRequestORM) -> UserResponseORM:
        async with PostgreSQLConnectionManager.get_session() as session:
            user_id = uuid4()
            stmt = insert(UserORM).values(id=user_id,
                                          login=user.login,
                                          name=user.name,
                                          hashed_password=user.hashed_password)
            await session.execute(stmt)
        return UserResponseORM(user_id, user.login, user.name, user.hashed_password)