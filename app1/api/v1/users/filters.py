from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from app1.core.models import User


class UserFilter(Filter):
    email__like: Optional[str] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)
    is_verified: Optional[bool] = Field(default=None)
    is_superuser: Optional[bool] = Field(default=None)

    class Constants(Filter.Constants):
        model = User

    class Config:
        populated_by_name = True
