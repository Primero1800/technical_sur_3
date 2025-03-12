from typing import TYPE_CHECKING

from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from sqlalchemy import Integer

from app1.api.v1.schemas.user import UserRead, UserCreate
from app1.core.config import fastapi_users_config

if TYPE_CHECKING:
    pass

fastapi_users = FastAPIUsers["User", Integer](
    fastapi_users_config.get_user_manager,
    [fastapi_users_config.authentication_backend],
)

router = APIRouter()

# /login
# /logout
router.include_router(
    fastapi_users.get_auth_router(fastapi_users_config.authentication_backend)
)

# /register
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
