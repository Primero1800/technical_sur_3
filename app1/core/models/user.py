from typing import TYPE_CHECKING

from fastapi_users.db import (
    SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase,
)

from app1.core.models.base import Base
from app1.core.models.mixins import IDIntPkMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, IDIntPkMixin, SQLAlchemyBaseUserTable[int]):

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session,  cls)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, email={self.email})"

    def __repr__(self):
        return str(self)
