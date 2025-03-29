import logging
from typing import TYPE_CHECKING, Sequence, Any

from fastapi import UploadFile
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app1.core.models import Rubric, RubricImage
from app1.exceptions import CustomException
from ..utils.image_utils import save_image

if TYPE_CHECKING:
    from .schemas import (
        RubricCreate,
    )


CLASS = "Rubric"
_CLASS = "rubric"

logger = logging.getLogger(__name__)


async def get_all(
    session: AsyncSession,
) -> Sequence:
    stmt = select(Rubric).options(joinedload(Rubric.image), joinedload(Rubric.products))
    result: Result = await session.execute(stmt)
    return result.unique().scalars().all()


async def create_one(
    session: AsyncSession,
    instance: "RubricCreate",
    image_schema: UploadFile,
) -> Rubric:

    orm_model: Rubric = Rubric(**instance.model_dump())

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
        image: RubricImage | None = RubricImage(file=file_path, rubric_id=orm_model.id)
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
    orm_model: Rubric,
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
) -> Rubric:
    if id:
        stmt = select(Rubric).where(Rubric.id == id).options(
            joinedload(Rubric.image), joinedload(Rubric.products)
        ).order_by(Rubric.id)
    else:
        stmt = select(Rubric).where(Rubric.slug == slug).options(
            joinedload(Rubric.image), joinedload(Rubric.products)
        ).order_by(Rubric.id)
    result: Result = await session.execute(stmt)
    orm_model: Rubric | None = result.unique().scalar_one_or_none()

    if not orm_model:
        text_error = f"id={id}" if id else f"slug={slug!r}"
        raise CustomException(
            msg=f"{CLASS} with {text_error} not found"
        )
    return orm_model


async def edit_one(
    orm_model: Rubric,
    instance: Any,
    image_schema: UploadFile,
    session: AsyncSession,
    is_partial: bool = False
) -> Rubric:

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

        image: RubricImage | None = None
        try:
            stmt = select(RubricImage).where(RubricImage.rubric_id == orm_model.id)
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
