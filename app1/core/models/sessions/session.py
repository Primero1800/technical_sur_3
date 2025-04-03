from datetime import datetime
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy.generics import TIMESTAMPAware, now_utc
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app1.core.config import DBConfigurer
from app1.core.models import Base

if TYPE_CHECKING:
    from app1.core.models import User


class Session(Base):
    session_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(f"{DBConfigurer.utils.camel2snake('User')}.id", ondelete="CASCADE"),
        nullable=True,
        unique=True,
    )
    user_email: Mapped[str] = mapped_column(nullable=True)
    data: Mapped[str]
    expired_at: Mapped[datetime] = mapped_column(
        TIMESTAMPAware(timezone=True), index=True, nullable=False, default=now_utc
    )

    user: Mapped['User'] = relationship(
        'User',
        back_populates='user',
    )