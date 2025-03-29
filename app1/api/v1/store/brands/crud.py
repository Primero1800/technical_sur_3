import logging
from typing import TYPE_CHECKING, Sequence, Any

from fastapi import UploadFile
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app1.core.models import (
    Brand, BrandImage,
    Product,
)
from app1.exceptions import CustomException
from ..utils.image_utils import save_image

if TYPE_CHECKING:
    from .schemas import (
        BrandCreate,
    )


CLASS = "Brand"
_CLASS = "brand"

logger = logging.getLogger(__name__)


async def get_all(
    session: AsyncSession,
) -> Sequence:
    stmt = select(
        Brand,
    ).options(joinedload(Brand.image)).order_by(Brand.id)

    result: Result = await session.execute(stmt)
    return result.unique().scalars().all()


async def get_all_full(
    session: AsyncSession,
) -> Sequence:
    stmt = select(
        Brand,
        Product,
    ).options(joinedload(Brand.image), joinedload(Brand.products), joinedload(Product.images)).order_by(Brand.id)

    result: Result = await session.execute(stmt)
    return result.unique().scalars().all()


async def create_one(
    session: AsyncSession,
    instance: "BrandCreate",
    image_schema: UploadFile,
) -> Brand:

    orm_model: Brand = Brand(**instance.model_dump())

    try:
        session.add(orm_model)
        await session.commit()
        await session.refresh(orm_model)
        logger.info(f"{CLASS} {orm_model!r} was successfully created")
    except IntegrityError as error:
        logger.error(f"Error {error!r} while {orm_model!r} creating")
        raise CustomException(
            msg=f"{CLASS} {orm_model.title!r} already exists"
        )
    except Exception as error:
        logger.error(f"Error {error!r} while {orm_model!r} creating")
        raise error

    try:
        file_path: str = await save_image(
            image_object=image_schema,
            path=f"app1/media/{_CLASS}s",
            folder=f"{orm_model.id}"
        )
    except Exception as exc:
        logger.error(f"Error wile writing file {file_path!r}")
        raise exc

    logger.info(f"Image {image_schema!r} was successfully written")

    try:
        image: BrandImage | None = BrandImage(file=file_path, brand_id=orm_model.id)
        session.add(image)
        await session.commit()
        logger.info(f"{CLASS}Image {image!r} was successfully created")
    except IntegrityError as error:
        logger.error(f"Error {error!r} while {image!r} for {orm_model} creating. {orm_model!r} will be deleted")

        await delete_one(
            orm_model=orm_model,
            session=session,
        )
        raise CustomException(
            msg=f"Error {error!r} while {image!r} for {orm_model} creating."
        )

    return await get_one_complex(
        id=orm_model.id,
        session=session,
    )


async def delete_one(
    orm_model: Brand,
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


async def get_one_complex(
    session: AsyncSession,
    id: int = None,
    slug: str = None,
) -> Brand:

    stmt_select = select(
        Brand,
        Product,
    )
    if id:
        stmt_filter = stmt_select.where(Brand.id == id)
    else:
        stmt_filter = stmt_select.where(Brand.slug == slug)

    stmt = stmt_filter.options(
        joinedload(Brand.image), joinedload(Brand.products), joinedload(Product.images)
    ).order_by(Brand.id)

    result: Result = await session.execute(stmt)
    orm_model: Brand | None = result.unique().scalar_one_or_none()

    if not orm_model:
        text_error = f"id={id}" if id else f"slug={slug!r}"
        raise CustomException(
            msg=f"{CLASS} with {text_error} not found"
        )
    return orm_model


async def edit_one(
    orm_model: Brand,
    instance: Any,
    image_schema: UploadFile,
    session: AsyncSession,
    is_partial: bool = False
) -> Brand:

    for key, val in instance.model_dump(
        exclude_unset=is_partial,
        exclude_none=is_partial,
    ).items():
        setattr(orm_model, key, val)

    logger.warning(f"Editing {orm_model!r} in database")
    try:
        await session.commit()
        await session.refresh(orm_model)
    except IntegrityError as exc:
        logger.error(f"Error while editing {orm_model!r} in database: {exc!r}")
        raise CustomException(
            msg=f"Error while editing {orm_model!r} in database: {exc!r}"
        )

    if image_schema:
        try:
            file_path: str = await save_image(
                image_object=image_schema,
                path=f"app1/media/{_CLASS}s",
                folder=f"{orm_model.id}"
            )
        except Exception as exc:
            logger.error(f"Error while writing file {file_path!r}")
            raise exc
        logger.info(f"Image {image_schema!r} was successfully written")

        image: BrandImage | None = None
        try:
            stmt = select(BrandImage).where(BrandImage.brand_id == orm_model.id)
            image = await session.scalar(stmt)
            if image.file != file_path:
                image.file = file_path
                logger.warning(f"Editing {image!r} in database")
                await session.commit()
        except IntegrityError as exc:
            logger.error(f"Error while editing {CLASS}Image {image} in database: {exc}")
            raise CustomException(
                msg=f"{exc}"
            )

    orm_model = await get_one_complex(id=orm_model.id, session=session)
    return orm_model
