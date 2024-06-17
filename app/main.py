from fastapi import FastAPI
from .routers import router

app = FastAPI(
    title="ToDo Application",
    description="API для управления задачами",
    version="1.0.0",
)

app.include_router(router)
