from logging import Logger
from typing import TYPE_CHECKING

from fastapi_users import models, BaseUserManager

from app1.core.settings import settings

if TYPE_CHECKING:
    from app1.core.models import User
    from fastapi import Request


logger = settings.logging.LOGGER

async def hook_after_registration(
    request: "Request",
    user: "User",
    user_manager: BaseUserManager[models.UP, models.ID],
    logger: Logger = logger
):

    logger.warning("In after-registration-hook: user=%s", user)
    from app1.api.v1.auth.views import request_verify_token
    await request_verify_token(
        request=request,
        email=user.email,
        user_manager=user_manager,
    )

    # async with aiohttp.ClientSession() as session:
    #     async with session.post(
    #             url=f"{settings.run.app1.APP_HOST_SERVER_URL}{settings.auth.REQUEST_VERIFY_TOKEN_URL}",
    #             json={
    #                 "email": user.email
    #             }
    #     ) as response:
    #         response_data = await response.json(content_type="application/json")
    #         logger.info("Sent webhook, got response %s", response_data)
    # if response.status != 200:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=response_data['detail'] if "detail" in response_data else "Bad request. Verification error."
    #     )
    #
    # return response_data