from typing import TYPE_CHECKING, List, Sequence

from fastapi import APIRouter, UploadFile, Form, File, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app1.exceptions import CustomException
from .schemas import BrandCreate, BrandRead
from . import crud, utils
from . import dependencies as deps

from app1.core.auth.fastapi_users_config import current_superuser
from app1.core.config import DBConfigurer

if TYPE_CHECKING:
    from app1.core.models.store import Brand

router = APIRouter()


@router.get(
    "/",
    response_model=List[BrandRead],
    status_code=status.HTTP_200_OK,
)
async def get_all(
        session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> List[BrandRead]:
    listed_brands = await crud.get_all(
        session=session
    )
    result = []
    for brand in listed_brands:
        result.append(await utils.get_brand_schema_from_orm(orm_model=brand))
    return result


@router.post(
    "/",
    dependencies=[Depends(current_superuser),],
    status_code=status.HTTP_201_CREATED,
)
async def create_brand(
    # instance: BrandCreate = Form(...),
    title: str = Form(),
    description: str = Form(),
    image: UploadFile = File(),
    session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> None:
    try:
        instance: BrandCreate = BrandCreate(title=title, description=description)
        await crud.create_brand(
            instance=instance,
            image_schema=image,
            session=session,
        )
    except (CustomException, Exception) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.msg if hasattr(exc, "msg") else str(exc)
        )


@router.get(
    "/{brand_id}/",
    status_code=status.HTTP_200_OK,
    response_model=BrandRead,
)
async def get_one(
    brand_id: int,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
):
    try:
        brand = await crud.get_one_complex(
            brand_id=brand_id,
            session=session,
        )
        return await utils.get_brand_schema_from_orm(orm_model=brand)

    except (CustomException, Exception) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.msg if hasattr(exc, "msg") else str(exc)
        )


@router.delete(
    "/{brand_id}/",
    dependencies=[Depends(current_superuser), ],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_one(
    brand: "Brand" = Depends(deps.get_one_simple),
    session: AsyncSession = Depends(DBConfigurer.session_getter),
):
    try:
        await crud.delete_one(
            brand=brand,
            session=session,
        )
    except (CustomException, Exception) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.msg if hasattr(exc, "msg") else str(exc)
        )
