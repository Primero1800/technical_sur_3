from typing import TYPE_CHECKING
from fastapi import Depends
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase

from app1.core.config import DBConfigurer
from app1.core.models import AccessToken

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_token_db(
    session: "AsyncSession" = Depends(DBConfigurer.session_getter)
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)