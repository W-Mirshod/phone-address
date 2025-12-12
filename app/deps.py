from redis.asyncio import Redis
from app.config import get_redis_client


async def get_redis() -> Redis:
    return get_redis_client()

