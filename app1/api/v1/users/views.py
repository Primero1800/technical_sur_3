from typing import Optional

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
        page: int = Query(1, gt=0),
        size: int = Query(10, gt=0),
        sort_by: Optional[str] = None,
        user_filter: UserFilter = FilterDepends(UserFilter),
        session: AsyncSession = Depends(DBConfigurer.session_getter),
) -> list[UserRead]:

    result_full = await crud.get_all_users(
        session=session,
        filter_model=user_filter,
    )

    from app1.scripts.pagination import paginate_result
    return await paginate_result(
        query_list=result_full,
        page=page,
        size=size,
        sort_by=sort_by,
    )


@router.post(
    '/create-form',
    response_model=UserRead
)
async def create_user_throw_form(
        user: UserCreateStraight = Form(),
) -> UserRead:
    return await crud.create_user_throw_form(
        instance=user,
    )
