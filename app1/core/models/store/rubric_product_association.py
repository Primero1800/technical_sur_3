from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app1.core.models import (
    Base, Product,
    Rubric,
)
from app1.core.models.mixins import IDIntPkMixin


class RubricProductAssociation(IDIntPkMixin, Base):
    __table_args__ = (
        UniqueConstraint("rubric_id", "product_id", name="idx_unique_rubric_product"),
    )

    rubric_id: Mapped[int] = mapped_column(ForeignKey(Rubric.id))
    product_id: Mapped[int] = mapped_column(ForeignKey(Product.id))
