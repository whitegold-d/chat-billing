import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.model.ORM.base import Base


class TransactionORM(Base):
    __tablename__ = 'transactions'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    transaction_type: Mapped[str] = mapped_column()
    value: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    user: Mapped["UserORM"] = relationship(back_populates="transactions")