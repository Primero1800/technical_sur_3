from typing import TYPE_CHECKING

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
)
from fastapi import Depends
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy
from sqlalchemy import Integer

from app1.core.settings import settings

from app1.api.v1.auth.dependencies.users import get_user_db
from app1.api.v1.auth.dependencies.access_token import get_access_token_db
from app1.api.v1.auth.dependencies.user_manager import get_user_manager

if TYPE_CHECKING:
    from app1.core.models import AccessToken


# Strategy

def get_database_strategy(
    access_token_db: AccessTokenDatabase["AccessToken"] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db,
        lifetime_seconds=settings.access_token.ACCESS_TOKEN_LIFETIME,
    )


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
