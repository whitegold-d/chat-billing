from fastapi import FastAPI

from app.router.auth_router import auth_router
from app.router.chat_router import chat_router

app = FastAPI(title="billing-app", description="", version="1.0")
app.include_router(router=auth_router, prefix="/api/v1")
app.include_router(router=chat_router, prefix="/api/v1")