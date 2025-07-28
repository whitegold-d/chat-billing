from typing import Annotated

from fastapi import Depends

from app.infrastructure.db.initialize.implementation.sqlite_database import SQLiteDatabase
from app.infrastructure.db.initialize.interface.base_database import BaseDatabase
from app.service.implementation.db_service import DBService


def get_db() -> BaseDatabase:
    return SQLiteDatabase()

current_db = get_db()