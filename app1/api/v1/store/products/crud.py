import logging
from typing import TYPE_CHECKING, Sequence, Any, List

from asyncpg import UniqueViolationError
from fastapi import UploadFile
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app1.core.models import (
    Product,
    ProductImage,
    Brand,
    Rubric,
)
from app1.exceptions import CustomException
from ..utils.image_utils import save_image, del_directory

from app1.api.v1.store.brands.dependencies import get_one_simple as brands_deps_get_one
from app1.api.v1.store.rubrics.dependencies import get_one_simple as rubrics_deps_get_one

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
    stmt = select(Product).options(
        joinedload(Product.images),
        joinedload(Product.brand),
    ).order_by(Product.id)
    result: Result = await session.execute(stmt)
    return result.unique().scalars().all()


async def get_all_full(
    session: AsyncSession,
) -> Sequence:

    stmt = select(Product).options(
        joinedload(Product.images),
        joinedload(Product.rubrics).joinedload(Rubric.image),
        joinedload(Product.brand).joinedload(Brand.image),
    ).order_by(Product.id)

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
        logger.error(f"Error while deleting {CLASS!r} from database: {exc!r}")
        raise CustomException(
            msg=f"Error while deleting {CLASS!r} from database: {exc!r}"
        )


async def create_one(
    session: AsyncSession,
    instance: "ProductCreate",
    image_schemas: List[UploadFile],
    rubric_ids: List[int],
) -> Product:

    orm_model: Product = Product(
        **instance.model_dump(),
    )

    # CHECKING BRAND_ID VALIDATION

    brand_orm_model: "Brand" = await brand_id_validation(
        brand_id=instance.brand_id,
        session=session,
    )

    # CHECKING RUBRICS_IDS VALIDATION

    rubrics_orm_models: List["Rubric"] = await rubric_ids_validation(
        rubric_ids=rubric_ids,
        session=session
    )

    # CREATING PRODUCT IN DATABASE

    try:
        session.add(orm_model)
        for rubric_orm_model in rubrics_orm_models:
            orm_model.rubrics.append(rubric_orm_model)
        await session.commit()
        await session.refresh(orm_model)


    except IntegrityError as exc:
        if isinstance(exc.orig, UniqueViolationError):
            logger.error(f"Unique constraint violation while creating {CLASS!r}: {exc!r}")
            raise CustomException(
                msg=f"Unique constraint violation: {exc.orig}",
            )
        else:
            logger.error(f"General integrity error while creating {CLASS!r}: {exc!r}")
            raise CustomException(
                msg=f"Integrity error: {exc!r}",
            )
    except PendingRollbackError as exc:
        logger.error(f"Pending rollback error while creating {CLASS!r}: {exc!r}")
        raise CustomException(
            msg=f"Pending rollback error: {exc!r}",
        )

    logger.info(f"{CLASS} {orm_model!r} was successfully created")

    # WORKING WITH IMAGES

    folder: str = f"{orm_model.id}"
    path: str = f"app1/media/{_CLASS}s"
    file_pathes: list = []

    for index, image_schema in enumerate(image_schemas):
        try:
            file_path: str = await save_image(
                image_object=image_schema,
                path=path,
                folder=folder,
                cleaning=False,
                name=f"pic_{index}",
            )
            file_pathes.append(file_path)

        except Exception as error:
            logger.error(f"Error wile writing file {file_path!r}")
            await del_directory(folder=folder, path=path)
            await delete_one(
                orm_model=orm_model,
                session=session,
            )
            raise CustomException(
                msg=f"Error {error!r} while {image!r} for {orm_model} creating."
            )

        logger.info(f"Image {image_schema!r} was successfully written")

        try:
            image: ProductImage | None = ProductImage(file=file_path, product_id=orm_model.id)
            session.add(image)
            await session.commit()
            logger.info(f"{CLASS}Image {image!r} was successfully created")
        except IntegrityError as error:
            logger.error(f"Error {error!r} while {image!r} for {orm_model} creating. {orm_model!r} will be deleted")
            await del_directory(folder=folder, path=path)
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


async def get_one_complex(
    session: AsyncSession,
    id: int = None,
    slug: str = None,
) -> Product:

    stmt_select = select(Product)
    if id:
        stmt_filter = stmt_select.where(Product.id == id)
    else:
        stmt_filter = stmt_select.where(Product.slug == slug)

    stmt = stmt_filter.options(
        joinedload(Product.images),
        joinedload(Product.rubrics).joinedload(Rubric.image),
        joinedload(Product.brand).joinedload(Brand.image),
    )
    result: Result = await session.execute(stmt)
    orm_model: Product | None = result.unique().scalar()

    if not orm_model:
        text_error = f"id={id}" if id else f"slug={slug!r}"
        raise CustomException(
            msg=f"{CLASS} with {text_error} not found"
        )
    return orm_model


async def edit_one(
    orm_model: Product,
    instance: Any,
    image_schemas: List[UploadFile],
    rubric_ids: List[int],
    session: AsyncSession,
    is_partial: bool = False
) -> Product:

    # CHECKING BRAND_ID VALIDATION
    if  instance.brand_id or instance.brand_id == 0:
        brand_orm_model: "Brand" = await brand_id_validation(
            brand_id=instance.brand_id,
            session=session,
        )

    # CHECKING RUBRICS_IDS VALIDATION
    if rubric_ids:
        rubrics_orm_models: List["Rubric"] = await rubric_ids_validation(
            rubric_ids=rubric_ids,
            session=session
        )

    # EDITING PRODUCT IN DATABASE

    for key, val in instance.model_dump(
        exclude_unset=is_partial,
        exclude_none=is_partial,
    ).items():
        setattr(orm_model, key, val)

    logger.warning(f"Editing {orm_model!r} in database")

    if rubric_ids:
        orm_model.rubrics.clear()
        for rubric_orm_model in rubrics_orm_models:
            orm_model.rubrics.append(rubric_orm_model)

        try:
            await session.commit()
            await session.refresh(orm_model)
        except IntegrityError as exc:
            if isinstance(exc.orig, UniqueViolationError):
                logger.error(f"Unique constraint violation while editing {CLASS!r}: {exc!r}")
                raise CustomException(
                    msg=f"Unique constraint violation: {exc.orig}",
                )
            else:
                logger.error(f"General integrity error while editing {CLASS!r}: {exc!r}")
                raise CustomException(
                    msg=f"Integrity error: {exc!r}",
                )
        except PendingRollbackError as exc:
            logger.error(f"Pending rollback error while editing {CLASS!r}: {exc!r}")
            raise CustomException(
                msg=f"Pending rollback error: {exc!r}",
            )
        logger.info(f"{CLASS} {orm_model!r} was successfully edited")

    # WORKING WITH IMAGES

    if image_schemas:
        folder: str = f"{orm_model.id}"
        path: str = f"app1/media/{_CLASS}s"
        file_pathes: list = []
        old_images_ids: list = [image.id for image in orm_model.images]

        for index, image_schema in enumerate(image_schemas):
            try:
                file_path: str = await save_image(
                    image_object=image_schema,
                    path=path,
                    folder=folder,
                    cleaning=False,
                    name=f"pic_{index}",
                )
                file_pathes.append(file_path)

            except Exception as error:
                logger.error(f"Error wile writing file {file_path!r}")
                raise CustomException(
                    msg=f"Error {error!r} while {image!r} for {orm_model} editing."
                )

            logger.info(f"Image {image_schema!r} was successfully written")

            try:
                image: ProductImage | None = ProductImage(file=file_path, product_id=orm_model.id)
                session.add(image)
                await session.commit()
                logger.info(f"{CLASS}Image {image!r} was successfully edited")
            except IntegrityError as error:
                logger.error(f"Error while adding image: {error!r}")
                raise CustomException(
                    msg=f"Error while adding image: {error!r}"
                )

        logger.warning(f"Images was successfully added, while {orm_model} editing. Old images will be deleted from database.")

        # DELETING ALL PICTURES FROM DATABASE

        for old_image_id in old_images_ids:
            await delete_picture(
                session=session,
                id=old_image_id,
            )
        await session.refresh(orm_model)

    orm_model = await get_one_complex(id=orm_model.id, session=session)
    return orm_model


async def rubric_ids_validation(
    rubric_ids: List[int],
    session: AsyncSession,
) -> List["Rubric"]:
    rubric_ids_set = set(rubric_ids)
    rubrics_orm_models: List["Rubric"] = []
    for rubric_id in rubric_ids_set:
        rubric_orm_model: "Rubric" = await rubrics_deps_get_one(
            id=rubric_id,
            session=session,
        )
        rubrics_orm_models.append(rubric_orm_model)
    return rubrics_orm_models


async def brand_id_validation(
    session: AsyncSession,
    brand_id: int
) -> "Brand":
    return await brands_deps_get_one(
        id=brand_id,
        session=session,
    )


async def delete_picture(
    session: AsyncSession,
    id: int,
):
    try:
        old_image: ProductImage | None = await session.get(ProductImage, id)
        await session.delete(old_image)
        await session.commit()
    except IntegrityError as exc:
        logger.error(f"Error while deleting {CLASS!r} from database: {exc!r}")
        raise CustomException(
            msg=f"Error while deleting {CLASS!r} from database: {exc!r}"
    )
