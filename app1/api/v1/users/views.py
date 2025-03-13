from fastapi import APIRouter
from app1.api.v1.users.schemas import UserRead, UserUpdate

from app1.core.auth import fastapi_users


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
