from fastapi import APIRouter
from app1.api.v1.schemas.user import UserRead, UserUpdate

from app1.core.config.fastapi_users_config import fastapi_users

# from app1.core.config import  FastAPIUsersConfigurer

router = APIRouter()

# /api/v1/users/me GET
# /api/v1/users/me PATCH
# /api/v1/users/{id} GET
# /api/v1/users/{id} PATCH
# /api/v1/users/{id} DELETE
router.include_router(
    fastapi_users.get_users_router(
        UserRead, UserUpdate
    ),
)
