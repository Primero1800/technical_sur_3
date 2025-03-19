from typing import TYPE_CHECKING

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app1.scripts.create_user import create_user_straight as scripts_create_user_straight
from app1.core.models import User
from app1.api.v1.users.schemas import UserCreate

if TYPE_CHECKING:
    from app1.api.v1.users.schemas import UserCreateStraight


async def get_all_users(
        session: AsyncSession,
):
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    return result.scalars().all()


async def create_user_throw_form(
        instance: "UserCreateStraight",
):
    return await scripts_create_user_straight(
        instance=UserCreate(**instance.model_dump()),
    )
