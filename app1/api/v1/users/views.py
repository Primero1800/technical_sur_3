from fastapi import (
    APIRouter, Depends, Form, Request, Query,
)
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from app1.api.v1.users import crud
from app1.api.v1.users.filters import UserFilter
from app1.api.v1.users.schemas import (
    UserRead, UserUpdate, UserCreateStraight,
)

from app1.core.auth.fastapi_users_config import (
    fastapi_users,
    current_superuser
)
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
        session: AsyncSession = Depends(DBConfigurer.session_getter),
        user_filter: UserFilter = FilterDepends(UserFilter),
) -> list[UserRead]:
    return await crud.get_all_users(
        session=session,
        filter_model=user_filter,
    )


@router.post(
    '/create-form',
    response_model=UserRead
)
async def create_user_throw_form(
        user: UserCreateStraight = Form(),
) -> UserRead:
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ', UserCreateStraight.model_fields)
    return await crud.create_user_throw_form(
        instance=user,
    )
