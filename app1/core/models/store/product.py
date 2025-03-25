from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app1.core.models import (
    IDIntPkMixin, Base, TitleSlugModel, DescriptionMixin, Title3FieldMixin
)


class Product(IDIntPkMixin, Title3FieldMixin, TitleSlugModel, DescriptionMixin, Base):
    pass
