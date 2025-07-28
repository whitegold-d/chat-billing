import sqlite3
from typing import List, Optional
from uuid import uuid4

from app.infrastructure.db.model.request.user_request import UserRequestORM
from app.infrastructure.db.model.response.user_response import UserResponseORM
from app.infrastructure.db.repository.interface.base_user_repository import BaseUserRepository
from app.service.interface.base_db_service import BaseDBService
from app.utils.constants import DB_PATH


class SQLiteUserRepository(BaseUserRepository):
    _self = None

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    async def get_user_by_id(self, user_id: str) -> Optional[UserResponseORM]:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM user WHERE id = ?""", (user_id,))
            user = cursor.fetchone()
        if not user:
            return None
        user_response = UserResponseORM(*user)
        return user_response


    async def get_all_users(self, **filters) -> List[UserResponseORM] | None:
        result = []

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM user""")
            user_tuples = cursor.fetchall()

        if not user_tuples:
            return None

        users = [UserResponseORM(*user) for user in user_tuples]
        for key, value in filters.items():
            for user in users:
                if hasattr(user, key):
                    actual_value = getattr(user, key)
                    if actual_value == value:
                        result.append(user)

        return result


    async def save_user(self, user: UserRequestORM) -> UserResponseORM:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            user_id = uuid4()
            cursor.execute("""INSERT INTO user (id, login, name, hashed_password) VALUES (?, ?, ?, ?)""",
                           (str(user_id), user.login, user.name, user.hashed_password))
            conn.commit()
        return UserResponseORM(user_id, user.login, user.name, user.hashed_password)