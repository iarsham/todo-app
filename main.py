from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.router import todo_router

app = FastAPI()


@app.on_event("startup")
async def startup_db():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_NAME]


@app.on_event("shutdown")
async def shutdown_db():
    app.mongodb_client.close()


@app.get("/")
async def say_hello() -> dict:
    return {"response": "Hello World"}


app.include_router(todo_router, prefix="/todo")
