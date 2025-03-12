from typing import TYPE_CHECKING

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
)
from fastapi import Depends
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy
from sqlalchemy import Integer

from app1.core.config import DBConfigurer
from app1.core.settings import settings
from app1.core.authentication.user_manager import UserManager
from app1.core.models import User, AccessToken

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


# Access token

async def get_access_token_db(
    session: "AsyncSession" = Depends(DBConfigurer.session_getter)
):
    yield AccessToken.get_db(session=session)


# Strategy

def get_database_strategy(
    access_token_db: AccessTokenDatabase["AccessToken"] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db,
        lifetime_seconds=settings.access_token.ACCESS_TOKEN_LIFETIME,
    )


# Users

async def get_user_db(
        session: "AsyncSession" = Depends(DBConfigurer.session_getter)
):
    yield User.get_db(session=session)


# User_manager

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


# Backend

bearer_transport = BearerTransport(
    tokenUrl=settings.auth.TRANSPORT_TOKEN_URL
)


authentication_backend = AuthenticationBackend(
    name="access-token-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)


# FastAPI Users

fastapi_users = FastAPIUsers["User", Integer](
    get_user_manager,
    [authentication_backend],
)





