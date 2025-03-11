from typing import TYPE_CHECKING

from fastapi import Depends

from app1.core.models import User
from app1.core.config import DBConfigurer

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(session: "AsyncSession" = Depends(DBConfigurer.session_getter)):
    yield User.get_db(session=session)
