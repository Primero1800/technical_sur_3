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


async def delete_one(
    orm_model: Product,
    session: AsyncSession,
) -> None:
    try:
        logger.info(f"Deleting {orm_model!r} from database")
        await session.delete(orm_model)
        await session.commit()
    except IntegrityError as exc:
        logger.error(f"Error while deleting {orm_model!r} from database: {exc!r}")
        raise CustomException(
            msg=f"Error while deleting {orm_model!r} from database: {exc!r}"
        )