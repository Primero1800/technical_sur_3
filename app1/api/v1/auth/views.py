from fastapi import APIRouter

from app1.api.v1.schemas.user import UserRead, UserCreate
from app1.core.config import FastAPIUsersConfigurer


router = APIRouter()

# /login
# /logout
router.include_router(
    FastAPIUsersConfigurer.fastapi_users.get_auth_router(
        FastAPIUsersConfigurer.authentication_backend
    )
)

# /register
router.include_router(
    FastAPIUsersConfigurer.fastapi_users.get_register_router(UserRead, UserCreate),
)
