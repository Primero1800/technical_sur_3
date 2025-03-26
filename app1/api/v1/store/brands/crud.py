import logging
from typing import TYPE_CHECKING

from fastapi import UploadFile
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app1.core.models import Brand, BrandImage
from app1.exceptions import CustomException
from ..utils.image_utils import save_image
from .schemas import BrandRead

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
        logger.error(f"Error {error!r} while {brand!r} creating")
        raise CustomException(
            msg=f"Brand {brand.title!r} already exists"
        )
    except Exception as error:
        print('BRAND INTEGRITY ERROR: ', error)
        logger.error(f"Error {error!r} while {brand!r} creating")
        raise error

    try:
        file_path: str = await save_image(brand.id, image_schema, folder="app1/media/brands")
        logger.info(f"Image {image_schema!r} was successfully written")

        image: BrandImage = BrandImage(file=file_path, brand_id=brand.id)
        session.add(image)
        await session.commit()
        logger.info(f"BrandImage {image!r} was successfully created")

    except (IntegrityError, Exception) as error:
        print('BRAND INTEGRITY ERROR: ', error)
        logger.error(f"Error {error!r} while {image!r} for {brand.id} creating. Brand {brand!r} will be deleted")

        await session.delete(brand)
        await session.commit()

        raise error


async def get_one_simple(
    brand_id: int,
    session: AsyncSession,
) -> Brand:

    brand: Brand | None = await session.get(Brand, brand_id)

    if not brand:
        raise CustomException(
            msg=f"Brand with id={brand_id} not found"
        )
    return brand


async def get_one_complex(
    brand_id: int,
    session: AsyncSession,
) -> Brand:

    stmt = select(Brand).where(Brand.id == brand_id).options(joinedload(Brand.image))
    result: Result = await session.execute(stmt)
    brand: Brand | None = result.scalar_one_or_none()

    if not brand:
        raise CustomException(
            msg=f"Brand with id={brand_id} not found"
        )
    return brand


