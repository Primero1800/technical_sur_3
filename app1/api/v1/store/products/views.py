from typing import TYPE_CHECKING, List, Optional

from fastapi import APIRouter, UploadFile, Form, File, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app1.exceptions import CustomException
from .schemas import (
    ProductCreate, ProductRead, ProductShort,
    ProductUpdate, ProductPartialUpdate,
)
from . import crud, utils
from . import dependencies as deps

from app1.core.auth.fastapi_users_config import current_superuser
from app1.core.config import DBConfigurer

if TYPE_CHECKING:
    from app1.core.models import Product

router = APIRouter()


@router.get(
    "/",
    response_model=List[ProductShort],
    status_code=status.HTTP_200_OK,
)
async def get_all(
        session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> List[ProductShort]:
    listed_orm_models = await crud.get_all(
        session=session
    )
    result = []
    for orm_model in listed_orm_models:
        result.append(await utils.get_short_schema_from_orm(orm_model=orm_model))
    return result


@router.get(
    "/full/",
    dependencies=[Depends(current_superuser),],
    response_model=List[ProductRead],
    status_code=status.HTTP_200_OK,
)
async def get_all_full(
        session: AsyncSession = Depends(DBConfigurer.session_getter)
):
    listed_orm_models = await crud.get_all_full(
        session=session
    )
    result = []
    for orm_model in listed_orm_models:
        result.append(await utils.get_schema_from_orm(orm_model=orm_model))
    return result


@router.post(
    "/",
    dependencies=[Depends(current_superuser),],
    status_code=status.HTTP_201_CREATED,
    response_model=ProductRead,
)
async def create_one(
    title: str = Form(),
    description: str = Form(),
    brand_id: int = Form(),
    # rubric_ids: List[int] = Form(),
    rubric_ids: str = Form(...),
    images: List[UploadFile] = File(),
    session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> ProductRead:

    # TEMPORARY FRAGMENT    #####################################
    rubric_ids = await temporary_fragment(ids=rubric_ids)
    ############################################################

    # catching ValidationError in exception_handler
    instance: ProductCreate = ProductCreate(
        title=title,
        description=description,
        brand_id=brand_id,
    )

    try:
        orm_model = await crud.create_one(
            instance=instance,
            image_schemas=images,
            rubric_ids=rubric_ids,
            session=session,
        )
        return await utils.get_schema_from_orm(orm_model=orm_model)

    except CustomException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.msg,
        )


@router.get(
    "/{id}/",
    dependencies=[Depends(current_superuser),],
    status_code=status.HTTP_200_OK,
    response_model=ProductRead,
)
async def get_one(
    id: int,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
):
    try:
        orm_model = await crud.get_one_complex(
            id=id,
            session=session,
        )
        return await utils.get_schema_from_orm(orm_model=orm_model)

    except (CustomException, Exception) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.msg if hasattr(exc, "msg") else str(exc)
        )


@router.get(
    "/title/{slug}/",
    status_code=status.HTTP_200_OK,
    response_model=ProductRead,
)
async def get_one_by_slug(
    slug: str,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
):
    try:
        orm_model = await crud.get_one_complex(
            slug=slug,
            session=session,
        )
        return await utils.get_schema_from_orm(orm_model=orm_model)

    except (CustomException, Exception) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.msg if hasattr(exc, "msg") else str(exc)
        )


@router.delete(
    "/{id}/",
    dependencies=[Depends(current_superuser), ],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_one(
    orm_model: "Product" = Depends(deps.get_one_simple),
    session: AsyncSession = Depends(DBConfigurer.session_getter),
):
    try:
        await crud.delete_one(
            orm_model=orm_model,
            session=session,
        )
    except (CustomException, Exception) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.msg if hasattr(exc, "msg") else str(exc)
        )


@router.put(
    "/{id}/",
    dependencies=[Depends(current_superuser), ],
    status_code=status.HTTP_200_OK,
    response_model=ProductRead
)
async def edit_one(
    title: str = Form(),
    description: str = Form(),
    brand_id: int = Form(),
    rubric_ids: str = Form(...),
    images: List[UploadFile] = File(),
    session: AsyncSession = Depends(DBConfigurer.session_getter),
    orm_model: "Product" = Depends(deps.get_one_complex)
):

    # TEMPORARY FRAGMENT    #####################################
    rubric_ids = await temporary_fragment(ids=rubric_ids)
    ############################################################

    # catching ValidationError in exception_handler
    instance: ProductUpdate = ProductUpdate(
        title=title,
        description=description,
        brand_id=brand_id,
    )

    try:
        orm_model = await crud.edit_one(
            orm_model=orm_model,
            instance=instance,
            image_schemas=images,
            rubric_ids=rubric_ids,
            session=session,
        )
        return await utils.get_schema_from_orm(orm_model=orm_model)

    except CustomException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.msg,
        )


@router.patch(
    "/{id}/",
    dependencies=[Depends(current_superuser), ],
    status_code=status.HTTP_200_OK,
    response_model=ProductRead
)
async def edit_one(
    title: Optional[str] = Form(default=None),
    description: Optional[str] = Form(default=None),
    brand_id: Optional[int] = Form(default=None),
    rubric_ids: Optional[str] = Form(default=None),
    images: Optional[List[UploadFile]] = None,
    session: AsyncSession = Depends(DBConfigurer.session_getter),
    orm_model: "Product" = Depends(deps.get_one_complex)
):

    # TEMPORARY FRAGMENT    #####################################
    rubric_ids = await temporary_fragment(ids=rubric_ids)
    ############################################################

    # catching ValidationError in exception_handler
    instance: ProductPartialUpdate = ProductPartialUpdate(
        title=title,
        description=description,
        brand_id=brand_id,
    )

    try:
        orm_model = await crud.edit_one(
            orm_model=orm_model,
            instance=instance,
            image_schemas=images,
            rubric_ids=rubric_ids,
            session=session,
            is_partial=True,
        )
        return await utils.get_schema_from_orm(orm_model=orm_model)

    except CustomException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.msg,
        )


async def temporary_fragment(ids: str):
    try:
        return [int(el.strip()) for el in ids.split(',')] if ids else []
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parameter 'rubric_ids' must contains only integers, differed by comma"
        )
