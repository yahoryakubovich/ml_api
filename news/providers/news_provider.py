from sqlalchemy.ext.asyncio import AsyncSession

from news.repositories.news_repository import NewsRepository
from news.services.news_service import NewsService


def news_provider(session: AsyncSession) -> NewsService:
    repository = NewsRepository(session)
    service = NewsService(repository)
    return service
