from fastapi import Depends

import logging
from typing import Optional, TYPE_CHECKING, Union, Dict, Any
from sqlalchemy import Integer

from fastapi_users import BaseUserManager, IntegerIDMixin, schemas, models, InvalidPasswordException

from app1.core.settings import settings
from app1.core.auth.users import get_user_db

from app1.core.auth.webhooks.users_webhooks import hook_send_new_user_notification
from app1.scripts.mail_sender import send_mail
from app1.scripts.scrypt_schemas.email import CustomMessageSchema

if TYPE_CHECKING:
    from app1.core.models import User
    from fastapi import Request
    from starlette.responses import Response

log = logging.getLogger(__name__)

RESET_PASSWORD_TOKEN_SECRET = settings.access_token.RESET_PASSWORD_TOKEN_SECRET
VERIFICATION_TOKEN_SECRET = settings.access_token.VERIFICATION_TOKEN_SECRET
USERS_PASSWORD_MIN_LENGTH = settings.users.USERS_PASSWORD_MIN_LENGTH
VERIFICATION_TOKEN_LIFETIME_SECONDS = settings.access_token.VERIFICATION_TOKEN_LIFETIME_SECONDS


class UserManager(IntegerIDMixin, BaseUserManager["User", Integer]):
    reset_password_token_secret = RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = VERIFICATION_TOKEN_SECRET

    async def on_after_register(
            self,
            user: "User",
            request: Optional["Request"] = None
    ):

        log.warning("%r has registered." % (user, ))

        # webhook
        # await hook_send_new_user_notification(user)

        # mailsender
        schema = CustomMessageSchema(
            recipients=[user.email,],
            subject=settings.app.APP_TITLE + '. Registration',
            body=f"You have been registered on {settings.app.APP_TITLE}"
        )
        await send_mail(schema=schema)

    async def on_after_forgot_password(
        self, user: "User", token: str, request: Optional["Request"] = None
    ):
        log.warning("%r has forgot their password. Reset token: %r" % (user, token))

    async def on_after_reset_password(
            self, user: "User", request: Optional["Request"] = None):
        log.warning("%r has reset his password." % (user, ))

    async def on_after_request_verify(
        self, user: "User", token: str, request: Optional["Request"] = None
    ):
        log.warning("Verification requested for %r. Verification token: %r" % (user, token))

        schema = CustomMessageSchema(
            recipients=[user.email, ],
            subject=settings.app.APP_TITLE + '. Registration',
            body=f"You have been registered on {settings.app.APP_TITLE}. "
                 f"To finish registration, please, use this token in "
                 f"{settings.access_token.VERIFICATION_TOKEN_LIFETIME_SECONDS // 60} min: {token}"
        )
        await send_mail(schema=schema)

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
        if len(password) < USERS_PASSWORD_MIN_LENGTH:
            raise InvalidPasswordException(
                reason=f"Password should be at least {USERS_PASSWORD_MIN_LENGTH} characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)