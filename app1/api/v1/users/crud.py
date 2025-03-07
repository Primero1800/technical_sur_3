from typing import Sequence

from fastapi.exceptions import RequestValidationError
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app1.api.v1.users.schemas import UserCreate
from app1.core.models import User
from app1.core import errors


async def get_users(
        session: AsyncSession
) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    return result.scalars().all()


async def create_user(
        session: AsyncSession,
        instance: UserCreate
) -> User:
    user: User = User(**instance.model_dump())
    # try:
    session.add(user)
    await session.commit()
    # except IntegrityError as error:
    #     raise errors.Validation(
    #         msg=errors.get_message(error)
    #     )
    await session.refresh(user)
    return user
