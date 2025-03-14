from typing import Annotated

from fastapi_users import schemas
from pydantic import Field, EmailStr, BaseModel

from app1.api.v1.users.mixins import DisplayUserNameMixin
from app1.core.settings import settings


class UserRead(DisplayUserNameMixin, schemas.BaseUser[int]):
    pass


class UserCreate(DisplayUserNameMixin, schemas.BaseUserCreate):
    pass


class UserUpdate(DisplayUserNameMixin, schemas.BaseUserUpdate):
    pass


class UserCreateStraight(DisplayUserNameMixin):
    email: EmailStr
    password: Annotated[str, Field(
        min_length=settings.users.USERS_PASSWORD_MIN_LENGTH
    )]


class UserRegisteredWebhookNotification(BaseModel):
    user: UserRead
    time: str
