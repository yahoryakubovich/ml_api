import datetime
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from common.models.base import Base


class News(Base):
    __tablename__ = "news"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4())
    title: Mapped[str]
    description: Mapped[str]
    content: Mapped[str]
    is_verified: Mapped[bool] = mapped_column(server_default=expression.false(), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(nullable=True, onupdate=func.now())
