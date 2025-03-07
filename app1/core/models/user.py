from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app1.core.models import Base


class User(Base):
    username: Mapped[str] = mapped_column(
        unique=True,
        default='username',
    )
    foo: Mapped[str] = mapped_column(
        unique=False,
        default='foo',
        server_default='foo'
    )
    bar: Mapped[str] = mapped_column(
        unique=False,
        default='bar',
        server_default='bar'
    )

    __table_args__ = (
        UniqueConstraint('foo', 'bar'),
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username})"

    def __repr__(self):
        return str(self)
