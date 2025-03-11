from typing import TYPE_CHECKING

from fastapi import Depends

from app1.core.models import AccessToken
from app1.core.config import DBConfigurer

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_token_db(
    session: "AsyncSession" = Depends(DBConfigurer.session_getter)
):
    yield AccessToken.get_db(session=session)
