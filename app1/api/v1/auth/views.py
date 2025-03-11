from typing import TYPE_CHECKING

from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from sqlalchemy import Integer

from app1.api.dependencies.backend import authentication_backend
from app1.api.dependencies.user_manager import get_user_manager

if TYPE_CHECKING:
    from app1.core.models import User

fastapi_users = FastAPIUsers["User", Integer](
    get_user_manager,
    [authentication_backend],
)

router = APIRouter()
router.include_router(
    fastapi_users.get_auth_router(authentication_backend)
)
