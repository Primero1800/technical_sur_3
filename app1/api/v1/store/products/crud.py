import logging
from typing import TYPE_CHECKING, Sequence, Any

from fastapi import UploadFile
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app1.core.models import Product, ProductImage
from app1.exceptions import CustomException
from ..utils.image_utils import save_image

if TYPE_CHECKING:
    from .schemas import (
        ProductCreate,
    )


CLASS = "Product"
_CLASS = "product"


logger = logging.getLogger(__name__)


async def get_all(
    session: AsyncSession,
) -> Sequence:
    stmt = select(Product).options(joinedload(Product.images), joinedload(Product.rubrics), joinedload(Product.brand))
    result: Result = await session.execute(stmt)
    return result.unique().scalars().all()
