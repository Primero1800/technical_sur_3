import logging
import uuid
from typing import Optional, TYPE_CHECKING

from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin


from app1.core.settings import settings

if TYPE_CHECKING:
    from ..models import User
    from sqlalchemy import Integer
    from fastapi import Request

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager["User", Integer]):
    reset_password_token_secret = settings.access_token.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = settings.access_token.VERIFICATION_TOKEN_SECRET

    async def on_after_register(self, user: "User", request: Optional["Request"] = None):
        log.warning("%s has registered.".format(user))

    async def on_after_forgot_password(
        self, user: "User", token: str, request: Optional["Request"] = None
    ):
        log.warning("%r has forgot their password. Reset token: %r".format(user, token))

    async def on_after_request_verify(
        self, user: "User", token: str, request: Optional["Request"] = None
    ):
        log.warning(f"Verification requested for %r. Verification token: %r".format(user, token))
