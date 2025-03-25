from fastapi import APIRouter, UploadFile, Form, File, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import BrandCreate
from . import crud

from app1.core.auth.fastapi_users_config import current_superuser
from app1.core.config import DBConfigurer

router = APIRouter()


@router.post(
    "/",
    dependencies=[Depends(current_superuser),],
    status_code=status.HTTP_201_CREATED,
)
async def create_brand(
    instance: BrandCreate,
    image: UploadFile = File(),
    session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> None:
    try:
        await crud.create_brand(
            instance=instance,
            image_schema=image,
            session=session,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )

