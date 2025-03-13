from fastapi_users import schemas

from app1.api.v1.users.mixins import DisplayUserNameMixin


class UserRead(DisplayUserNameMixin, schemas.BaseUser[int]):
    pass


class UserCreate(DisplayUserNameMixin, schemas.BaseUserCreate):
    pass


class UserUpdate(DisplayUserNameMixin, schemas.BaseUserUpdate):
    pass
