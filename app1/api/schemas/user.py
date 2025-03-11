from fastapi_users import schemas
from sqlalchemy import Integer


class UserRead(schemas.BaseUser[Integer]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass