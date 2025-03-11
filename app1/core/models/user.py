from fastapi_users.db import (
    SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase,
)

from .base import Base
from .mixins import IDIntPkMixin


class User(Base, IDIntPkMixin, SQLAlchemyBaseUserTable[int]):
    pass
