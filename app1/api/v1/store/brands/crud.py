import logging
from typing import TYPE_CHECKING, Sequence, Any

from fastapi import UploadFile
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app1.core.models import Brand, BrandImage
from app1.exceptions import CustomException
from ..utils.image_utils import save_image

if TYPE_CHECKING:
    from .schemas import (
        BrandCreate, BrandUpdate, BrandPartialUpdate,
    )

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

    brand: Brand = Brand(**instance.model_dump())

    try:
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
        file_path: str = await save_image(
            image_object=image_schema,
            path="app1/media/brands",
            folder=f"{brand.id}_{brand.title}"
        )
    except Exception as exc:
        logger.error(f"Error wile writing file {file_path!r}")
        raise exc

    logger.info(f"Image {image_schema!r} was successfully written")

    try:
        image: BrandImage | None = BrandImage(file=file_path, brand_id=brand.id)
        session.add(image)
        await session.commit()
        logger.info(f"BrandImage {image!r} was successfully created")
    except IntegrityError as error:
        logger.error(f"Error {error!r} while {image!r} for {brand} creating. {brand!r} will be deleted")

        await delete_one(
            brand=brand,
            session=session,
        )
        raise CustomException(
            msg=f"Error {error!r} while {image!r} for {brand} creating."
        )

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
    session: AsyncSession,
    brand_id: int = None,
    slug: str = None,
) -> Brand:
    if brand_id:
        stmt = select(Brand).where(Brand.id == brand_id).options(joinedload(Brand.image))
    else:
        stmt = select(Brand).where(Brand.slug == slug).options(joinedload(Brand.image))
    result: Result = await session.execute(stmt)
    brand: Brand | None = result.scalar_one_or_none()

    if not brand:
        text_error = f"id={brand_id}" if brand_id else f"slug={slug!r}"
        raise CustomException(
            msg=f"Brand with {text_error} not found"
        )
    return brand


async def edit_brand(
    brand: Brand,
    instance: Any,
    image_schema: UploadFile,
    session: AsyncSession,
    is_partial: bool = False
) -> Brand:

    for key, val in instance.model_dump(
        exclude_unset=is_partial,
        exclude_none=is_partial,
    ).items():
        setattr(brand, key, val)

    logger.warning(f"Editing {brand!r} in database")
    try:
        await session.commit()
        await session.refresh(brand)
    except IntegrityError as exc:
        logger.error(f"Error while editing {brand!r} in database: {exc!r}")
        raise CustomException(
            msg=f"Error while editing {brand!r} in database: {exc!r}"
        )

    if image_schema:
        try:
            file_path: str = await save_image(
                image_object=image_schema,
                path="app1/media/brands",
                folder=f"{brand.id}_{brand.title}"
            )
        except Exception as exc:
            logger.error(f"Error while writing file {file_path!r}")
            raise exc
        logger.info(f"Image {image_schema!r} was successfully written")

        brand_image: BrandImage | None = None
        try:
            stmt = select(BrandImage).where(BrandImage.brand_id == brand.id)
            brand_image = await session.scalar(stmt)
            if brand_image.file != file_path:
                brand_image.file = file_path
                logger.warning(f"Editing {brand_image!r} in database")
                await session.commit()
        except IntegrityError as exc:
            logger.error(f"Error while editing BrandImage {brand_image} in database: {exc}")
            raise CustomException(
                msg=f"{exc}"
            )

    brand = await get_one_complex(brand_id=brand.id, session=session)
    return brand


