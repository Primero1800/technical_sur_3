import logging
from typing import TYPE_CHECKING, Sequence

from fastapi import UploadFile
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app1.core.models import Brand, BrandImage
from app1.exceptions import CustomException
from ..utils.image_utils import save_image

if TYPE_CHECKING:
    from .schemas import BrandCreate

logger = logging.getLogger(__name__)


async def get_all(
    session: AsyncSession,
) -> Sequence:
    stmt = select(Brand).options(joinedload(Brand.image))
    result: Result = await session.execute(stmt)
    return result.scalars().all()


async def create_brand(
    session: AsyncSession,
    instance: "BrandCreate",
    image_schema: UploadFile,
) -> Brand:
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
        logger.error(f"Error {error!r} while {brand!r} creating")
        raise error

    try:
        image: BrandImage | None
        file_path: str = await save_image(brand.id, image_schema, folder="app1/media/brands")
        logger.info(f"Image {image_schema!r} was successfully written")

        image = BrandImage(file=file_path, brand_id=brand.id)
        session.add(image)
        await session.commit()
        logger.info(f"BrandImage {image!r} was successfully created")

    except (IntegrityError, Exception) as error:
        logger.error(f"Error {error!r} while {image!r} for {brand} creating. {brand!r} will be deleted")

        await delete_one(
            brand=brand,
            session=session,
        )
        raise error

    return await get_one_complex(
        brand_id=brand.id,
        session=session,
    )


async def delete_one(
    brand: Brand,
    session: AsyncSession,
) -> None:
    try:
        logger.info(f"Deleting {brand!r} from database")
        await session.delete(brand)
        await session.commit()
    except IntegrityError as exc:
        logger.error(f"Error while deleting {brand!r} from database: {exc!r}")
        raise CustomException(
            msg=f"Error while deleting {brand!r} from database: {exc!r}"
        )


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


