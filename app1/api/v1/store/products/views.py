from typing import TYPE_CHECKING, List, Optional

from fastapi import APIRouter, UploadFile, Form, File, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app1.exceptions import CustomException
from .schemas import ProductCreate, ProductRead, ProductUpdate, ProductPartialUpdate
from . import crud, utils
from . import dependencies as deps

from app1.core.auth.fastapi_users_config import current_superuser
from app1.core.config import DBConfigurer

if TYPE_CHECKING:
    from app1.core.models import Product

router = APIRouter()


@router.get(
    "/",
    response_model=List[ProductRead],
    status_code=status.HTTP_200_OK,
)
async def get_all(
        session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> List[ProductRead]:
    listed_orm_models = await crud.get_all(
        session=session
    )
    result = []
    for orm_model in listed_orm_models:
        result.append(await utils.get_schema_from_orm(orm_model=orm_model))
    return result




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