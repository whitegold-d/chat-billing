import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.model.ORM.base import Base


class MessageORM(Base):
    __tablename__ = 'messages'

    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    chat_id: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column()
    text: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)