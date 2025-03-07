from sqlalchemy.orm import Mapped, mapped_column

from app1.core.models import Base


class User(Base):
    username: Mapped[str] = mapped_column(
        unique=True,
        default='username',
    )