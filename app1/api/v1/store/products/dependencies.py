from fastapi import Depends, HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app1.core.config import DBConfigurer
from app1.core.models import Product, Rubric, Brand

CLASS = "Product"


async def get_one_simple(
    id: int,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> Product:

    orm_model: Product | None = await session.get(Product, id)

    if not orm_model:
        raise HTTPException(
            detail=f"{CLASS} with id={id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return orm_model


async def get_one_complex(
    id: int = None,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> Product:

    stmt_select = select(Product).where(Product.id == id)
    stmt = stmt_select.options(
        joinedload(Product.images),
        joinedload(Product.rubrics).joinedload(Rubric.image),
        joinedload(Product.brand).joinedload(Brand.image),
    )
    result: Result = await session.execute(stmt)
    orm_model: Product | None = result.unique().scalar()

    if not orm_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{CLASS} with id={id} not found",
        )
    return orm_model
