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
    def det_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session,  cls)
