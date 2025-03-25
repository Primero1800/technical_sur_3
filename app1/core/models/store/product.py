from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app1.core.models import Base
from app1.core.models.mixins import (
    IDIntPkMixin, Title3FieldMixin, TitleSlugModel, DescriptionMixin,
)
from app1.core.models.store.image import ImageBase


class Product(IDIntPkMixin, Title3FieldMixin, TitleSlugModel, DescriptionMixin, Base):

    images: Mapped[List['ProductImage']] = relationship(back_populates="product")


class ProductImage(ImageBase):
    product_id: Mapped[int] = mapped_column(
            ForeignKey(Product.id),
            nullable=False,
            unique=False,
        )

    product: Mapped[Product] = relationship(Product, back_populates='images')
