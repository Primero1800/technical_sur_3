from fastapi import APIRouter, Depends

from app1.api.v1.users.schemas import UserRead
from app1.core.models import User
from app1.core.auth.fastapi_users_config import (
    current_user, current_superuser,
)


router = APIRouter()


@router.get("")
async def get_user_messages(
        user: User = Depends(current_user)
):
    return {
        "messages": "m1, m2, m3",
        "user schema": UserRead.model_validate(
            user, from_attributes=True),
    }


@router.get("/superuser")
async def get_superuser_messages():
    pass