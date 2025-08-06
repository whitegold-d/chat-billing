from app.infrastructure.db.initialize.interface.base_database import BaseDatabase
from app.service.interface.base_db_service import BaseDBService


class DBService(BaseDBService):
    _self = None

    def __new__(cls, db: BaseDatabase):
        if cls._self is None:
            cls._self = super().__new__(cls)
            cls._self.db = db
        return cls._self

    async def init_db(self) -> None:
        await self.db.initialize_db()