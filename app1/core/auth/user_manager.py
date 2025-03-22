from fastapi import Depends

import logging
from typing import Optional, TYPE_CHECKING, Union, Dict, Any
from sqlalchemy import Integer

from fastapi_users import (
    BaseUserManager, IntegerIDMixin, schemas, models, InvalidPasswordException, exceptions,
)

from app1.core.settings import settings
from app1.core.auth.users import get_user_db

from app1.scripts.scrypt_schemas.email import CustomMessageSchema

if TYPE_CHECKING:
    from app1.core.models import User
    from fastapi import Request, BackgroundTasks, Response


log = logging.getLogger(__name__)

RESET_PASSWORD_TOKEN_SECRET = settings.access_token.RESET_PASSWORD_TOKEN_SECRET
VERIFICATION_TOKEN_SECRET = settings.access_token.VERIFICATION_TOKEN_SECRET
USERS_PASSWORD_MIN_LENGTH = settings.users.USERS_PASSWORD_MIN_LENGTH
VERIFICATION_TOKEN_LIFETIME_SECONDS = settings.access_token.VERIFICATION_TOKEN_LIFETIME_SECONDS
RESET_PASSWORD_TOKEN_LIFETIME_SECONDS = settings.access_token.RESET_PASSWORD_TOKEN_LIFETIME_SECONDS


class UserManager(IntegerIDMixin, BaseUserManager["User", Integer]):
    reset_password_token_secret = RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = VERIFICATION_TOKEN_SECRET

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional["Request"] = None,
        background_tasks: Optional["BackgroundTasks"] = None,
    ) -> models.UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param background_tasks: Optional for usings BackgroundTasks inside manager
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request, background_tasks)

        return created_user

    async def on_after_register(
            self,
            user: "User",
            request: Optional["Request"] = None,
            background_tasks: Optional["BackgroundTasks"] = None,
    ):
        log.warning("%r has registered." % (user, ))

        # webhooks

        # from app1.core.auth.webhooks.users_webhooks import hook_send_new_user_notification
        # await hook_send_new_user_notification(user)

        from app1.scripts.after_registration import hook_after_registration
        await hook_after_registration(
            user_manager=self,
            request=request,
            user=user,
        )

        # mailsender

        # schema = CustomMessageSchema(
        #     recipients=[user.email,],
        #     subject=settings.app.APP_TITLE + '. Registration',
        #     body=f"You have been registered on {settings.app.APP_TITLE}"
        # )
        # await send_mail(
        #     schema=schema,
        #     background_tasks=background_tasks
        # )

    async def on_after_forgot_password(
        self, user: "User", token: str, request: Optional["Request"] = None
    ):
        log.warning("%r has forgot their password. Reset token: %r" % (user, token))
        schema = CustomMessageSchema(
            recipients=[user.email, ],
            subject=settings.app.APP_TITLE + '. Password changing.',
            body=f"You have been requested on {settings.app.APP_TITLE} "
                 f"for password restoring, please, use this token in "
                 f"{RESET_PASSWORD_TOKEN_LIFETIME_SECONDS // 60} min: {token}   /n or just follow"
                 f" the link: {settings.run.app1.APP_HOST_SERVER_URL}{settings.auth.RESET_PASSWORD_HOOK_TOKEN_URL}/?token={token}"
        )

        # from app1.scripts.mail_sender.utils import send_mail
        # await send_mail(schema=schema)

        from app1.api.v1.celery_tasks.tasks import task_send_mail
        task_send_mail.apply_async(args=(schema.model_dump(),))

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
                 f"{VERIFICATION_TOKEN_LIFETIME_SECONDS // 60} min: {token}   /n or just follow"
                 f" the link: {settings.run.app1.APP_HOST_SERVER_URL}{settings.auth.VERIFY_HOOK_TOKEN_URL}/?token={token}"
        )

        # from app1.scripts.mail_sender.utils import send_mail
        # await send_mail(schema=schema)

        from app1.api.v1.celery_tasks.tasks import task_send_mail
        task_send_mail.apply_async(args=(schema.model_dump(), ))

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
