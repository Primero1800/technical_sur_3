import logging
from typing import Sequence, TYPE_CHECKING, Any

from fastapi import UploadFile
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app1.core.models import (
    Rubric,
    RubricImage,
)
from app1.exceptions import CustomException
from ..utils.image_utils import save_image

if TYPE_CHECKING:
    from .schemas import (
        RubricCreate,
    )

logger = logging.getLogger(__name__)


async def get_all(
    session: AsyncSession,
) -> Sequence:
    stmt = select(Rubric).options(joinedload(Rubric.image), joinedload(Rubric.products))
    result: Result = await session.execute(stmt)
    return result.scalars().all()


async def create_rubric(
    session: AsyncSession,
    instance: "RubricCreate",
    image_schema: UploadFile,
) -> Rubric:

    rubric: Rubric = Rubric(**instance.model_dump())

    try:
        session.add(rubric)
        await session.commit()
        await session.refresh(rubric)
        logger.info(f"Rubric {rubric!r} was successfully created")
    except IntegrityError as error:
        logger.error(f"Error {error!r} while {rubric!r} creating")
        raise CustomException(
            msg=f"Rubric {rubric.title!r} already exists"
        )
    except Exception as error:
        logger.error(f"Error {error!r} while {rubric!r} creating")
        raise error

    try:
        file_path: str = await save_image(
            image_object=image_schema,
            path="app1/media/rubrics",
            folder=f"{rubric.id}"
        )
    except Exception as exc:
        logger.error(f"Error wile writing file {file_path!r}")
        raise exc

    logger.info(f"Image {image_schema!r} was successfully written")

    try:
        image: RubricImage | None = RubricImage(file=file_path, rubric_id=rubric.id)
        session.add(image)
        await session.commit()
        logger.info(f"RubricImage {image!r} was successfully created")
    except IntegrityError as error:
        logger.error(f"Error {error!r} while {image!r} for {rubric} creating. {rubric!r} will be deleted")

        await delete_one(
            rubric=rubric,
            session=session,
        )
        raise CustomException(
            msg=f"Error {error!r} while {image!r} for {rubric} creating."
        )

    return await get_one_complex(
        rubric_id=rubric.id,
        session=session,
    )


async def delete_one(
    rubric: Rubric,
    session: AsyncSession,
) -> None:
    try:
        logger.info(f"Deleting {rubric!r} from database")
        await session.delete(rubric)
        await session.commit()
    except IntegrityError as exc:
        logger.error(f"Error while deleting {rubric!r} from database: {exc!r}")
        raise CustomException(
            msg=f"Error while deleting {rubric!r} from database: {exc!r}"
        )


async def get_one_complex(
    session: AsyncSession,
    rubric_id: int = None,
    slug: str = None,
) -> Rubric:
    print("IIIIIIIINNN GET ONE COMPLEX ", rubric_id, slug)
    if rubric_id:
        stmt = select(Rubric).where(Rubric.id == rubric_id).options(joinedload(Rubric.image), joinedload(Rubric.products))
    else:
        stmt = select(Rubric).where(Rubric.slug == slug).options(joinedload(Rubric.image), joinedload(Rubric.products))
    result: Result = await session.execute(stmt)
    rubric: Rubric | None = result.unique().scalar_one_or_none()

    if not rubric:
        text_error = f"id={rubric_id}" if rubric_id else f"slug={slug!r}"
        raise CustomException(
            msg=f"Rubric with {text_error} not found"
        )
    return rubric


async def edit_rubric(
    rubric: Rubric,
    instance: Any,
    image_schema: UploadFile,
    session: AsyncSession,
    is_partial: bool = False
) -> Rubric:

    for key, val in instance.model_dump(
        exclude_unset=is_partial,
        exclude_none=is_partial,
    ).items():
        setattr(rubric, key, val)

    logger.warning(f"Editing {rubric!r} in database")
    try:
        await session.commit()
        await session.refresh(rubric)
    except IntegrityError as exc:
        logger.error(f"Error while editing {rubric!r} in database: {exc!r}")
        raise CustomException(
            msg=f"Error while editing {rubric!r} in database: {exc!r}"
        )

    if image_schema:
        try:
            file_path: str = await save_image(
                image_object=image_schema,
                path="app1/media/rubrics",
                folder=f"{rubric.id}"
            )
        except Exception as exc:
            logger.error(f"Error while writing file {file_path!r}")
            raise exc
        logger.info(f"Image {image_schema!r} was successfully written")

        rubric_image: RubricImage | None = None
        try:
            stmt = select(RubricImage).where(RubricImage.rubric_id == rubric.id)
            rubric_image = await session.scalar(stmt)
            if rubric_image.file != file_path:
                rubric_image.file = file_path
                logger.warning(f"Editing {rubric_image!r} in database")
                await session.commit()
        except IntegrityError as exc:
            logger.error(f"Error while editing RubricImage {rubric_image} in database: {exc}")
            raise CustomException(
                msg=f"{exc}"
            )

    rubric = await get_one_complex(rubric_id=rubric.id, session=session)
    return rubric
