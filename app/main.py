from fastapi import FastAPI
from app.routers import router
from db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ToDo Application",
    description="API для управления задачами",
    version="1.0.0",
)

app.include_router(router)
