from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app1.core.config import DBConfigurer
from app1.core.models import Rubric

CLASS = "Rubric"


async def get_one_simple(
    id: int,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> Rubric:

    orm_model: Rubric | None = await session.get(Rubric, id)

    if not orm_model:
        raise HTTPException(
            detail=f"{CLASS} with id={id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return orm_model
