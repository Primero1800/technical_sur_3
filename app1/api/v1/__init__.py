from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from app1.core.settings import settings
from app1.api.v1.auth import router as auth_router
from app1.api.v1.users import router as users_router
from app1.api.v1.users import messages_router
from app1.api.v1.dependencies_example import router as deps_router

from app1.api.v1.webhooks import router as webhooks_router

http_bearer = HTTPBearer(
    auto_error=False
)

router = APIRouter(
    dependencies=[Depends(http_bearer)]
)

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

router.include_router(
    messages_router,
    prefix=settings.tags.USERS_MESSAGES_PREFIX,
    tags=[settings.tags.USERS_TAG],
)

router.include_router(
    deps_router,
    prefix=settings.tags.DEPENDENCIES_PREFIX,
    tags=[settings.tags.DEPENDENCIES_TAG],
)
