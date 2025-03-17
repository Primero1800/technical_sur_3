from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyBaseAccessTokenTable,
)
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app1.core.models import Base, User


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[int]):
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(User.id, ondelete="cascade"),
        nullable=False,
    )

    def __str__(self):
        return f"{self.__class__.__name__}(user_id={self.user_id}, created_at={self.created_at!r})"
