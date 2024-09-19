from typing import Optional, Sequence
from uuid import UUID

from loguru import logger
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.models import News
from common.schemas.news_schema import NewsCreateSchema, NewsUpdateSchema


class NewsRepository:
    model = News

    def __init__(self, session: AsyncSession):
        self.session = session
        logger.info("NewsRepository initialized with session: {session}", session=session)

    async def retrieve_all(self, limit: int = 10, offset: int = 0) -> Sequence[News]:
        logger.info("Retrieving all news with limit={limit} and offset={offset}", limit=limit, offset=offset)
        stmt = select(self.model).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        news = result.scalars().unique().all()
        logger.info("Retrieved {count} news", count=len(news))
        return news

    async def create(self, data: NewsCreateSchema) -> News:
        logger.info("Creating news with data: {data}", data=data.dict())
        news = self.model(**data.model_dump(exclude_unset=True))
        self.session.add(news)
        await self.session.flush()
        await self.session.refresh(news)
        logger.info("Created news with UUID: {uuid}", uuid=news.uuid)
        return news

    async def retrieve(self, uuid: UUID) -> Optional[News]:
        logger.info("Retrieving news with UUID: {uuid}", uuid=uuid)
        stmt = select(self.model).where(self.model.uuid == uuid)
        result = await self.session.execute(stmt)
        news = result.scalar()
        if news:
            logger.info("Retrieved news: {news}", news=news)
        else:
            logger.warning("No news found with UUID: {uuid}", uuid=uuid)
        return news

    async def update(self, uuid: UUID, data: NewsUpdateSchema) -> News:
        logger.info("Updating news with UUID: {uuid} using data: {data}", uuid=uuid, data=data.dict())
        stmt = (
            update(self.model)
            .where(self.model.uuid == uuid)
            .values(data.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        news = result.scalar()
        logger.info("Updated news: {news}", news=news)
        return news

    async def delete(self, uuid: UUID) -> None:
        logger.info("Deleting news with UUID: {uuid}", uuid=uuid)
        stmt = delete(self.model).where(self.model.uuid == uuid)
        await self.session.execute(stmt)
        logger.info("Deleted news with UUID: {uuid}", uuid=uuid)
