from sqlalchemy.orm import Mapped

from app1.core.models import Base
from app1.core.models.mixins import IDIntPkMixin


class ImageBase(IDIntPkMixin, Base):
    __abstract__ = True

    file: Mapped[str]
