from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status
from fastapi_cache.decorator import cache

from common.database import get_async_session
from common.models import News
from common.schemas.news_schema import (
    NewsCreateSchema,
    NewsRetrieveSchema,
    NewsUpdateSchema,
)
from news.providers.news_provider import news_provider

router = APIRouter(prefix="/news", tags=["news"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[NewsRetrieveSchema])
@cache(10)
async def retrieve_all_news(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)) -> Sequence[News]:
    async with get_async_session() as session:
        service = news_provider(session)
        return await service.retrieve_all_news(limit, offset)


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=NewsRetrieveSchema)
async def create_news(data: NewsCreateSchema) -> News:
    async with get_async_session() as session:
        service = news_provider(session)
        return await service.create_news(data)


@router.get("/{uuid}", status_code=status.HTTP_200_OK, response_model=NewsRetrieveSchema)
@cache(10)
async def retrieve_news(uuid: UUID) -> News:
    async with get_async_session() as session:
        service = news_provider(session)
        news = await service.retrieve_news(uuid)
        if not news:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News not found")
        return news


@router.patch("/{uuid}", status_code=status.HTTP_200_OK, response_model=NewsRetrieveSchema)
async def update_news(uuid: UUID, data: NewsUpdateSchema) -> News:
    async with get_async_session() as session:
        service = news_provider(session)
        return await service.update_news(uuid, data)


@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_news(uuid: UUID) -> None:
    async with get_async_session() as session:
        service = news_provider(session)
        await service.delete_news(uuid)
