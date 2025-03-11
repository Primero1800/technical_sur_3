from fastapi_users.db import (
    SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase,
)

from app1.core.models.base import Base
from app1.core.models.mixins import IDIntPkMixin


class User(Base, IDIntPkMixin, SQLAlchemyBaseUserTable[int]):
    pass
