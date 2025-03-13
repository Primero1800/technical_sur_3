from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app1.api.v1.users import crud
from app1.api.v1.users.schemas import UserRead, UserUpdate, UserCreate

from app1.core.auth import (
    fastapi_users,
    current_superuser
)
from app1.core.models import User
from app1.core.config import DBConfigurer

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


@router.get(
    '/',
    response_model=list[UserRead],
    dependencies=[Depends(current_superuser),],
)
async def get_users(
        session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> list[UserRead]:
    return await crud.get_all_users(session=session)
