from fastapi import APIRouter

from app1.core.settings import settings
from app1.api.v1.auth import router as auth_router
from app1.api.v1.users import router as users_router

router = APIRouter()

router.include_router(
    auth_router,
    prefix=settings.tags.AUTH_PREFIX,
    tags=[settings.tags.AUTH_TAG,],
)

router.include_router(
    users_router,
    prefix=settings.tags.USERS_PREFIX,
    tags=[settings.tags.USERS_TAG,],
)