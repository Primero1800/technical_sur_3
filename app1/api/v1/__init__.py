from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from app1.core.settings import settings
from app1.api.v1.auth import router as auth_router
from app1.api.v1.users import router as users_router
from app1.api.v1.users import messages_router
from app1.api.v1.sessions import router as sessions_router
from app1.api.v1.dependencies_example import router as deps_router
from app1.api.v1.celery_tasks import router as celery_router
from app1.api.v1.store import router as store_router

from app1.api.v1.webhooks import router as webhooks_router
from app1.api.v1.technical import router as technical_router


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

router.include_router(
    celery_router,
    prefix=settings.tags.CELERY_PREFIX,
    tags=[settings.tags.CELERY_TAG],
)

router.include_router(
    store_router,
)

router.include_router(
    technical_router,
    tags=[settings.tags.TECH_TAG]
)

router.include_router(
    sessions_router,
    prefix=settings.tags.SESSIONS_PREFIX,
    tags=[settings.tags.SESSIONS_TAG],
)
