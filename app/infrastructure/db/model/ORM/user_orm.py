import uuid
from typing import List
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.model.ORM.base import Base
from app.infrastructure.db.model.ORM.transaction_orm import TransactionORM


class UserORM(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(default=uuid.uuid4)
    login: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()

    transactions: Mapped[List["TransactionORM"]] = relationship(back_populates="user", cascade="all")