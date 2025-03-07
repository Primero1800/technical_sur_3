from fastapi import APIRouter

from app1.core.settings import settings
from app1.api.v1.users.views import router as users_router

router = APIRouter()

router.include_router(
    users_router,
    tags=[settings.tags.USERS_TAG,],
)