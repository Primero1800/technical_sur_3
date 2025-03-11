from fastapi import Depends

from app1.core.authentication.user_manager import UserManager
from .users import get_user_db


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)