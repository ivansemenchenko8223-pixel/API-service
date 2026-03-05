from fastapi import FastAPI
from app.api.v1.routers import router
from app.database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API для получения секретного ключа сотрудника",
    version="1.0.0")

app.include_router(router, prefix="/api/v1")