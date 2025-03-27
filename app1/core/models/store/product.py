from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app1.core.models import Base
from app1.core.models.mixins import (
    IDIntPkMixin, Title3FieldMixin, DescriptionMixin,
)
from app1.core.models.store.image import ImageBase


class Product(IDIntPkMixin, Title3FieldMixin, DescriptionMixin, Base):
    slug: Mapped[str]
    images: Mapped[List['ProductImage']] = relationship(
        'ProductImage',
        back_populates="product",
        cascade="all, delete",
    )

    def __str__(self):
        return f"Product(id={self.id}, title={self.title})"

    def __repr__(self):
        return str(self)


class ProductImage(ImageBase):
    product_id: Mapped[int] = mapped_column(
            ForeignKey(Product.id, ondelete="CASCADE"),
            nullable=False,
            unique=False,
        )

    product: Mapped[Product] = relationship(
        Product,
        back_populates='images'
    )

    def __str__(self):
        return f"ProductImage(product_id={self.product_id})"

    def __repr__(self):
        return str(self)
