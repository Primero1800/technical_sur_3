from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app1.core.models import (
    IDIntPkMixin, Base, DescriptionMixin, Title3FieldMixin,
)


class Brand(IDIntPkMixin, Title3FieldMixin, DescriptionMixin, Base):
    pass
