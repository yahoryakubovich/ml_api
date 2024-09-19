from typing import Optional, Sequence
from uuid import UUID

from loguru import logger

from common.models import News
from common.schemas.news_schema import NewsCreateSchema, NewsUpdateSchema
from news.repositories.news_repository import NewsRepository


class NewsService:
    def __init__(self, repository: NewsRepository):
        self._repository = repository
        logger.info("NewsService initialized with repository: {repository}", repository=repository)

    async def retrieve_all_news(self, limit: int = 10, offset: int = 0) -> Sequence[News]:
        logger.info("Retrieving all news with limit={limit} and offset={offset}", limit=limit, offset=offset)
        news = await self._repository.retrieve_all(limit, offset)
        logger.info("Retrieved {count} news", count=len(news))
        return news

    async def create_news(self, data: NewsCreateSchema) -> News:
        logger.info("Creating news with data: {data}", data=data.dict())
        news = await self._repository.create(data)
        logger.info("Created news with UUID: {uuid}", uuid=news.uuid)
        return news

    async def retrieve_news(self, uuid: UUID) -> Optional[News]:
        logger.info("Retrieving news with UUID: {uuid}", uuid=uuid)
        news = await self._repository.retrieve(uuid)
        if news:
            logger.info("Retrieved news: {news}", news=news)
        else:
            logger.warning("No news found with UUID: {uuid}", uuid=uuid)
        return news

    async def update_news(self, uuid: UUID, data: NewsUpdateSchema) -> News:
        logger.info("Updating news with UUID: {uuid} using data: {data}", uuid=uuid, data=data.dict())
        news = await self._repository.update(uuid, data)
        logger.info("Updated news: {news}", news=news)
        return news

    async def delete_news(self, uuid: UUID) -> None:
        logger.info("Deleting news with UUID: {uuid}", uuid=uuid)
        await self._repository.delete(uuid)
        logger.info("Deleted news with UUID: {uuid}", uuid=uuid)
