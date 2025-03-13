from fastapi_users import schemas

from app1.api.v1.users.mixins import DisplayUserNameMixin


class UserBase(DisplayUserNameMixin, schemas.BaseUser[int]):
    pass


class UserRead(UserBase):
    pass


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass
