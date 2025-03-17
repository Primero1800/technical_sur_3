from fastapi import APIRouter

from app1.api.v1.users.schemas import UserRead, UserCreate

from app1.core.auth.fastapi_users_config import (
    fastapi_users, authentication_backend,
)


router = APIRouter()

# /login
# /logout
router.include_router(
    fastapi_users.get_auth_router(
        authentication_backend,
        requires_verification=True,
    )
)

# /register
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)


# /request-verify-token
# /verify
router.include_router(
    fastapi_users.get_verify_router(UserRead),
)


# /forgot-password
# /reset-password
router.include_router(
    fastapi_users.get_reset_password_router(),
)
