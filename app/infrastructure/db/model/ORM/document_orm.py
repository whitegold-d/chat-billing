import uuid
from typing import List
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from app.infrastructure.db.model.ORM.base import Base


class DocumentsORM(Base):
    __tablename__ = 'documents'

    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    text: Mapped[str] = mapped_column()
    embedding: Mapped[List[float]] = mapped_column(Vector(768))