from fastapi import Depends

from app1.api.v1.auth.dependencies.users import get_user_db
from app1.core.authentication.user_manager import UserManager


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)