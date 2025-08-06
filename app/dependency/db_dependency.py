from app.infrastructure.db.initialize.implementation.postgresql_database import PostgreSQLDatabase
from app.infrastructure.db.initialize.interface.base_database import BaseDatabase


def get_db() -> BaseDatabase:
    # return SQLiteDatabase()
    return PostgreSQLDatabase()

current_db = get_db()