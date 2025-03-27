from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app1.core.models.mixins import (
    IDIntPkMixin, DescriptionMixin, Title3FieldMixin,
)
from app1.core.models.store.image import ImageBase
from app1.core.models import Base


class Brand(IDIntPkMixin, Title3FieldMixin, DescriptionMixin, Base):
    slug: Mapped[str]
    image: Mapped['BrandImage'] = relationship(
        "BrandImage",
        back_populates="brand",
        cascade="all, delete",
    )

    def __str__(self):
        return f"Brand(id={self.id}, title={self.title})"

    def __repr__(self):
        return str(self)


class BrandImage(ImageBase):
    brand_id: Mapped[int] = mapped_column(
            ForeignKey(Brand.id, ondelete="CASCADE"),
            nullable=False,
            unique=True,
        )

    brand: Mapped[Brand] = relationship(Brand, back_populates='image')

    def __str__(self):
        return f"BrandImage(brand_id={self.brand_id})"

    def __repr__(self):
        return str(self)
