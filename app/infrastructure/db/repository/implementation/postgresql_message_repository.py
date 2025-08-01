import asyncpg

from app.infrastructure.db.model.request.message_request import MessageRequestORM
from app.infrastructure.db.repository.interface.base_message_repository import BaseMessageRepository
from app.utils.constants import PG_DATABASE_DSN


class PostgreSQLMessageRepository(BaseMessageRepository):
    dsn = PG_DATABASE_DSN
    _self = None

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    async def get_all_messages(self, **filters):
        pass

    async def create_message(self, data: MessageRequestORM):
        pass