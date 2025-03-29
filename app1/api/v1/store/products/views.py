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
    from app1.core.models import Brand

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