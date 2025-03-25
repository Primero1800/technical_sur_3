import logging
from sqlite3 import IntegrityError
from typing import TYPE_CHECKING

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app1.core.models import Brand, BrandImage
from ..utils.image_utils import save_image

if TYPE_CHECKING:
    from .schemas import BrandCreate

logger = logging.getLogger(__name__)


async def create_brand(
    session: AsyncSession,
    instance: "BrandCreate",
    image_schema: UploadFile,
):
    try:
        brand: Brand = Brand(**instance.model_dump())
        session.add(brand)
        await session.commit()
        await session.refresh(brand)
        logger.info(f"Brand {brand!r} was successfully created")
    except IntegrityError as error:
        print('BRAND INTEGRITY ERROR: ', error)
        logger.error(f"Error {error!r} while {brand!r} creating")
        raise error

    try:
        await save_image(brand.id, image_schema, folder="app1/media/brands")

        image: BrandImage = BrandImage(**image_schema.model_dump(), brand_id=brand.id)
        session.add(image)
        await session.commit()
        logger.info(f"BrandImage {image!r} was successfully created")
    except IntegrityError as error:
        print('BRAND INTEGRITY ERROR: ', error)
        logger.error(f"Error {error!r} while {image!r} for {brand.id} creating. Brand {brand!r} will be deleted")
        await session.delete(brand)
        raise error


