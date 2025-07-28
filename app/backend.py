from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.dependency.db_dependency import current_db
from app.router.auth_router import auth_router
from app.router.chat_router import chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    current_db.init_db()
    yield


app = FastAPI(title="billing-app", description="", version="1.0", lifespan=lifespan)
app.include_router(router=auth_router, prefix="/api/v1")
app.include_router(router=chat_router, prefix="/api/v1")