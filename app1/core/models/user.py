from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app1.core.models import Base


class User(Base):
    username: Mapped[str] = mapped_column(
        unique=True,
        default='username',
    )
    # foo: Mapped[str]
    # bar: Mapped[str]
    #
    # __table_args__ = (
    #     UniqueConstraint('foo', 'bar'),
    # )