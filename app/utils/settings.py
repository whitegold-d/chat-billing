from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = Field(default="")
    DB_PORT: int = Field(default=5432)
    DB_USER: str = Field(default="")
    DB_PASS: str = Field(default="")
    DB_NAME: str = Field(default="")

    @property
    def db_dsn(self):
        # return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"postgresql+asyncpg://dev_user:pass@localhost:5432/my_app_dev"
