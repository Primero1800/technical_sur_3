import logging
from logging import Logger
from typing import TYPE_CHECKING

from fastapi_users import models, BaseUserManager


if TYPE_CHECKING:
    from app1.core.models import User
    from fastapi import Request


async def hook_after_registration(
    request: "Request",
    user: "User",
    user_manager: BaseUserManager[models.UP, models.ID],
    logger: Logger = logging.getLogger(__name__),
):
    logger.warning("In after-registration-hook: user=%s", user)

    if not user.is_verified:
        from app1.api.v1.auth.views import request_verify_token
        await request_verify_token(
            request=request,
            email=user.email,
            user_manager=user_manager,
        )
