from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app1.core.config import DBConfigurer
from app1.core.models import Brand
from app1.exceptions import CustomException


async def get_one_simple(
    brand_id: int,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> Brand:

    brand: Brand | None = await session.get(Brand, brand_id)

    if not brand:
        raise HTTPException(
            detail=f"Brand with id={brand_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return brand
