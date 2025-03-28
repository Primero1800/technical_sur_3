from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app1.core.config import DBConfigurer
from app1.core.models import Brand

CLASS = "Brand"


async def get_one_simple(
    id: int,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> Brand:

    orm_model: Brand | None = await session.get(Brand, id)

    if not orm_model:
        raise HTTPException(
            detail=f"{CLASS} with id={id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return orm_model
