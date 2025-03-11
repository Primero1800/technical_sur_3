from typing import TYPE_CHECKING

from fastapi import Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import Integer

from .user_manager import get_user_manager
from .backend import authentication_backend
from app1.core.models import User
from app1.core.config import DBConfigurer

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(
        session: "AsyncSession" = Depends(DBConfigurer.session_getter)
):
    yield User.get_db(session=session)


fastapi_users = FastAPIUsers[User, Integer](
    get_user_manager,
    [authentication_backend],
)
