from typing import List

from fastapi import APIRouter, status, Depends, Form, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app1.core.auth.fastapi_users_config import current_superuser
from app1.core.config import DBConfigurer
from app1.exceptions import CustomException
from . import crud, utils
from . import dependencies as deps
from .schemas import (
    RubricRead,
    RubricCreate,
)

router = APIRouter()


@router.get(
    "/",
    response_model=List[RubricRead],
    status_code=status.HTTP_200_OK,
)
async def get_all(
        session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> List[RubricRead]:
    listed_brands = await crud.get_all(
        session=session
    )
    result = []
    for brand in listed_brands:
        result.append(await utils.get_schema_from_orm(orm_model=brand))
    return result


@router.post(
    "/",
    dependencies=[Depends(current_superuser),],
    status_code=status.HTTP_201_CREATED,
    response_model=RubricRead,
)
async def create_rubric(
    title: str = Form(),
    description: str = Form(),
    image: UploadFile = File(),
    session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> RubricRead:

    # catching ValidationError in exception_handler
    instance: RubricCreate = RubricCreate(title=title, description=description)

    try:
        rubric = await crud.create_rubric(
            instance=instance,
            image_schema=image,
            session=session,
        )
        return await utils.get_schema_from_orm(orm_model=rubric)

    except (CustomException, Exception) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.msg if hasattr(exc, "msg") else str(exc)
        )


@router.get(
    "/{rubric_id}/",
    dependencies=[Depends(current_superuser),],
    status_code=status.HTTP_200_OK,
    response_model=RubricRead,
)
async def get_one(
    rubric_id: int,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
):
    try:
        rubric = await crud.get_one_complex(
            rubric_id=rubric_id,
            session=session,
        )
        return await utils.get_schema_from_orm(orm_model=rubric)

    except (CustomException, Exception) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.msg if hasattr(exc, "msg") else str(exc)
        )


@router.get(
    "/title/{slug}/",
    status_code=status.HTTP_200_OK,
    response_model=RubricRead,
)
async def get_one_by_slug(
    slug: str,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
):
    try:
        rubric = await crud.get_one_complex(
            slug=slug,
            session=session,
        )
        return await utils.get_schema_from_orm(orm_model=rubric)

    except (CustomException, Exception) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.msg if hasattr(exc, "msg") else str(exc)
        )


@router.delete(
    "/{rubric_id}/",
    dependencies=[Depends(current_superuser), ],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_one(
    rubric: "Rubric" = Depends(deps.get_one_simple),
    session: AsyncSession = Depends(DBConfigurer.session_getter),
):
    try:
        await crud.delete_one(
            rubric=rubric,
            session=session,
        )
    except (CustomException, Exception) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.msg if hasattr(exc, "msg") else str(exc)
        )
