from fastapi import APIRouter

from .user import router as user_webhooks_router

router = APIRouter()

router.include_router(user_webhooks_router)