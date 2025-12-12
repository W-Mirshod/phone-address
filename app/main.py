from fastapi import FastAPI
from app.api import router
from app.config import close_redis

app = FastAPI(
    title="Phone-Address Service",
    description="Microservice for storing and managing phone-address pairs",
    version="1.0.0"
)

app.include_router(router)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    await close_redis()

