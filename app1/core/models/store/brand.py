from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app1.core.models.mixins import (
    IDIntPkMixin, DescriptionMixin, Title3FieldMixin,
)
from app1.core.models.store.image import ImageBase
from app1.core.models import Base


class Brand(IDIntPkMixin, Title3FieldMixin, DescriptionMixin, Base):
    image: Mapped['BrandImage'] = relationship(back_populates="brand")


class BrandImage(ImageBase):
    brand_id: Mapped[int] = mapped_column(
            ForeignKey(Brand.id, ondelete="CASCADE"),
            nullable=False,
            unique=True,
        )

    brand: Mapped[Brand] = relationship(Brand, back_populates='image')
