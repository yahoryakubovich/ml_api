import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from common.config.config import settings
from news.routers.api import router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    logging.info("Running lifespan")
    redis = aioredis.from_url(settings.redis.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    logging.info("Redis initialized")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
