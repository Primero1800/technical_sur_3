from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app1.core.config.db_config import DBConfigurerInitializer
from app1.core.models import Base
from app1.core.models.mixins import (
    IDIntPkMixin, Title3FieldMixin, DescriptionMixin,
)
from app1.core.models.store.image import ImageBase
from app1.core.config.db_config import DBConfigurer

if TYPE_CHECKING:
    from app1.core.models import (
        Rubric,
        Brand,
    )


class Product(IDIntPkMixin, Title3FieldMixin, DescriptionMixin, Base):
    slug: Mapped[str]
    images: Mapped[List['ProductImage']] = relationship(
        'ProductImage',
        back_populates="product",
        cascade="all, delete",
    )

    rubrics: Mapped[list['Rubric']] = relationship(
        secondary=DBConfigurerInitializer.utils.camel2snake('RubricProductAssociation'),
        back_populates="products",
        # overlaps="orders_details",
    )

    brand_id: Mapped[int] = mapped_column(
        ForeignKey(f"{DBConfigurer.utils.camel2snake('Brand')}.id", ondelete="CASCADE"),
        nullable=False,
        unique=False,
    )

    brand: Mapped['Brand'] = relationship(
        'Brand',
        back_populates='products',
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
