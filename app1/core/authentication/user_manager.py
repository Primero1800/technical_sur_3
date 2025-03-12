import logging
from typing import Optional, TYPE_CHECKING, Union, Dict, Any
from sqlalchemy import Integer

from fastapi_users import BaseUserManager, IntegerIDMixin, schemas, models, InvalidPasswordException

from app1.core.settings import settings


if TYPE_CHECKING:
    from ..models import User
    from fastapi import Request
    from starlette.responses import Response

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager["User", Integer]):
    reset_password_token_secret = settings.access_token.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = settings.access_token.VERIFICATION_TOKEN_SECRET

    async def on_after_register(self, user: "User", request: Optional["Request"] = None):
        log.warning("%r has registered." % (user, ))

    async def on_after_forgot_password(
        self, user: "User", token: str, request: Optional["Request"] = None
    ):
        log.warning("%r has forgot their password. Reset token: %r" % (user, token))

    async def on_after_reset_password(
            self, user: "User", request: Optional["Request"] = None):
        log.warning("%r has reset their password." % (user, ))

    async def on_after_request_verify(
        self, user: "User", token: str, request: Optional["Request"] = None
    ):
        log.warning("Verification requested for %r. Verification token: %r" % (user, token))

    async def on_after_update(
            self, user: "User", update_dict: Dict[str, Any],
            request: Optional["Request"] = None,
    ):
        log.warning("%r has been updated with %r" % (user, update_dict))

    async def on_after_delete(
            self, user: "User", request: Optional["Request"] = None):
        log.info("%r is successfully deleted" % (user, ))

    async def on_after_login(
            self, user: "User",
            request: Optional["Request"] = None,
            response: Optional["Response"] = None,
    ):
        log.info("%r logged in." % (user,))

    async def validate_password(
        self, password: str, user: Union[schemas.UC, models.UP]
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )
