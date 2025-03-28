from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app1.core.config import DBConfigurer
from app1.core.models import Rubric


async def get_one_simple(
    rubric_id: int,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> Rubric:

    rubric: Rubric | None = await session.get(Rubric, rubric_id)

    if not rubric:
        raise HTTPException(
            detail=f"Rubric with id={rubric_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return rubric
