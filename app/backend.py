from fastapi import FastAPI

from app.router.auth_router import router

app = FastAPI(title="billing-app", description="", version="1.0")
app.include_router(router=router)