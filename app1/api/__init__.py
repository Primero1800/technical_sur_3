from fastapi import APIRouter

from app1.core.settings import settings
from app1.api.v1 import (
    router as v1_router,
    webhooks_router as v1_webhooks_router,
)

router = APIRouter()


router.include_router(
    v1_router,
    prefix=settings.app.API_V1_PREFIX
)

webhooks_router = v1_webhooks_router
