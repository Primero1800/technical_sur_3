from typing import TYPE_CHECKING

from fastapi import Depends
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy

from . import access_token
from app1.core.settings import settings

if TYPE_CHECKING:
    from app1.core.models import AccessToken


def get_database_strategy(
    access_token_db: AccessTokenDatabase["AccessToken"] = Depends(access_token.get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db,
        lifetime_seconds=settings.access_token.ACCESS_TOKEN_LIFETIME,
    )
