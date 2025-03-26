from fastapi import Depends
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
        raise CustomException(
            msg=f"Brand with id={brand_id} not found"
        )
    return brand