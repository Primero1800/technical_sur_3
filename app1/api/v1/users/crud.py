from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app1.core.models import User


async def get_all_users(
        session: AsyncSession,
):
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    return result.scalars().all()