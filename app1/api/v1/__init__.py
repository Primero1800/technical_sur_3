from fastapi import APIRouter

from app1.core.settings import settings
from app1.api.v1.auth import router as auth_router

router = APIRouter()

router.include_router(
    auth_router,
    prefix=settings.tags.AUTH_PREFIX,
    tags=[settings.tags.AUTH_TAG,],
)