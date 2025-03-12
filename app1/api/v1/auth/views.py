from fastapi import APIRouter

from app1.api.v1.schemas.user import UserRead, UserCreate

from app1.core.auth.fastapi_users_config import (
    fastapi_users, authentication_backend,
)


router = APIRouter()

# /login
# /logout
router.include_router(
    fastapi_users.get_auth_router(
        authentication_backend
    )
)

# /register
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
