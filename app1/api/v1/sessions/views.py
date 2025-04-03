import logging
from datetime import datetime
from typing import Any, Optional, TYPE_CHECKING, Dict
from uuid import uuid4, UUID

from fastapi import APIRouter, Response, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app1.api.v1.users.schemas import UserRead
from app1.core.auth.fastapi_users_config import current_user, fastapi_users, current_user_or_none
from app1.core.auth.user_manager import get_user_manager
from app1.core.config import DBConfigurer
from app1.core.sessions import fastapi_session_config as fs

if TYPE_CHECKING:
    from app1.core.models import User


logger = logging.getLogger(__name__)


router = APIRouter()


async def get_current_user_safe(user: Any = Depends(current_user)) -> Optional["User"]:
    print(1)
    try:
        return user
    except Exception as exc:
        logger.error("inside safe get user ", exc_info=exc)
        return None


async def get_current_user_safe2(
    user: Any = Depends(current_user)
) -> Any | None:
    print(1)
    return user if user else None


async def get_current_user_safe3() -> Optional["User"]:
    try:
        user = await current_user()
        return user
    except HTTPException as exc:
        if exc.status_code == status.HTTP_401_UNAUTHORIZED:
            return None  # Или можно выполнить какое-то логирование
        raise exc  # Если это не 401 ошибка, выбрасываем дальше


async def get_current_user_safe4(request: Request) -> Optional["User"]:
    try:
        user = await fastapi_users.current_user(active=True, verified=True)(request)
        return user
    except HTTPException as exc:
        if exc.status_code == status.HTTP_401_UNAUTHORIZED:
            # Логируем ошибку если нужно
            return None
        raise


async def get_current_user_safe5(request: Request) -> Optional["User"]:
    try:
        # Попробуйте извлечь пользователя из зависимости
        user = await fastapi_users.current_user(active=True, verified=True)(request)
        return user
    except HTTPException as exc:
        if exc.status_code == status.HTTP_401_UNAUTHORIZED:
            # Возвращаем None вместо выбрасывания ошибки
            return None
        raise


async def get_current_user_safe6(request: Request) -> Optional["User"]:
    """
    Обертка для получения текущего пользователя.
    Если пользователь не аутентифицирован, возвращает None.
    """
    try:
        print(1)
        user = await current_user(user_manager=Depends(get_user_manager))
        print(11)
        return user
    except Exception as exc:
        print(2)
        logger.error("Catched ", exc_info=exc)
        return None


@router.post(
    "/create_session",
)
async def create_session(
    response: Response,
    user: Any = Depends(current_user_or_none),
    session: AsyncSession = Depends(DBConfigurer.session_getter),
):

    user_dict = UserRead(**user.to_dict()).model_dump() if user else None
    user_session_uuid = uuid4()

    data = fs.SessionData(user=user_dict, data={"day": "monday", "time": datetime.now()})

    await fs.backend.create(user_session_uuid, data)
    fs.cookie.attach_to_response(response, user_session_uuid)

    username = user.email if user and hasattr(user, "email") else "Anonimous"
    response.status_code = status.HTTP_200_OK
    return {
        "user": username,
        "response": {
            "headers": response.headers,
            "status": response.status_code,
        }
    }


@router.get(
    "/whoami",
    dependencies=[Depends(fs.cookie)]
)
async def whoami(
    session_data: fs.SessionData = Depends(fs.verifier)
):
    return session_data


@router.post(
    "/delete_session",
)
async def del_session(
    response: Response,
    session_id: UUID = Depends(fs.cookie)
):
    await fs.backend.delete(session_id)
    fs.cookie.delete_from_response(response)
    return "deleted session"


@router.post(
    "/update_session",
    dependencies=[Depends(fs.cookie)]
)
async def update_session(
    data: Dict[str, Any],
    session_id: UUID = Depends(fs.cookie),
    session_data: fs.SessionData = Depends(fs.verifier)
):

    session_data.data.update(data)
    await fs.backend.update(session_id, session_data)

    return "session updated"


@router.post(
    "/clear_session",
    dependencies=[Depends(fs.cookie)]
)
async def update_session(
        session_id: UUID = Depends(fs.cookie),
        session_data: fs.SessionData = Depends(fs.verifier)
):
    session_data.data.clear()
    await fs.backend.update(session_id, session_data)

    return "session cleared"
