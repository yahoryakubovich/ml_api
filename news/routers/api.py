from fastapi import APIRouter

from news.routers.v1 import news

router = APIRouter(prefix="/api/v1")

router.include_router(news.router)
