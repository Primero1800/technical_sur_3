from typing import TYPE_CHECKING

from fastapi_users.db import (
    SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase,
)
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app1.core.models.base import Base
from app1.core.models.mixins import IDIntPkMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from app1.core.models import Session


class User(Base, IDIntPkMixin, SQLAlchemyBaseUserTable[int]):
    display_name: Mapped[str] = mapped_column(
        default='Incognito', server_default='Noname',
        nullable=False, type_=String(50),
    )

    session: Mapped['Session'] = relationship(
        "Session",
        back_populates="user",
        cascade="all, delete",
    )

    def __str__(self):
        return (f"{self.__class__.__name__}("
                f"id={self.id}, "
                f"email={self.email}, "
                f"display_name={self.display_name}"
                f")")

    def __repr__(self):
        return str(self)
