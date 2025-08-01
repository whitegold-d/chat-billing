import sqlite3

from app.infrastructure.db.initialize.interface.base_database import BaseDatabase
from app.utils.constants import DB_PATH


class SQLiteDatabase(BaseDatabase):
    _self = None

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            return super().__new__(cls)
        return cls._self

    def init_db(self) -> None:
        with sqlite3.connect(DB_PATH) as db:
            cursor = db.cursor()
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user (
                        id TEXT PRIMARY KEY,
                        login TEXT NOT NULL,
                        name TEXT UNIQUE NOT NULL,
                        hashed_password TEXT NOT NULL)""", ())
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS transaction_model (
                        id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        transaction_type TEXT NOT NULL,
                        value INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(user_id) REFERENCES user(id))""", ())
            db.commit()
            print("SqliteDB Successfully Initialized")