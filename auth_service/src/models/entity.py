import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import Column, DateTime, ForeignKey, String, select
from sqlalchemy.dialects.postgresql import UUID

from src.db.postgres import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(50), nullable=True)
