from datetime import datetime
from typing import Optional

from pydantic import UUID4

from common.schemas.base_schema import BaseSchema


class NewsCreateSchema(BaseSchema):
    title: str
    description: str
    content: str


class NewsRetrieveSchema(BaseSchema):
    uuid: UUID4
    title: str
    description: str
    content: str
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


class NewsUpdateSchema(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    is_verified: Optional[bool] = None
