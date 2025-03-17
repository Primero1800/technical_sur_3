import contextlib
from typing import TYPE_CHECKING

from fastapi_users.exceptions import UserAlreadyExists

from app1.core.auth.users import get_user_db
from app1.core.auth.user_manager import get_user_manager
from app1.core.config import DBConfigurer


if TYPE_CHECKING:
    from logging import Logger
    from app1.api.v1.users.schemas import UserCreate
    from app1.core.auth.user_manager import UserManager
    from app1.core.models import User


async def create_user(
        user_manager: "UserManager",
        user_create: "UserCreate",
) -> "User":
    user = await user_manager.create(
        user_create=user_create,
        safe=False,
    )
    return user


async def create_user_straight(
        instance: "UserCreate",
        logger: "Logger" = None,
) -> "User":
    try:
        async with DBConfigurer.Session() as session:
            get_user_db_context = contextlib.asynccontextmanager(get_user_db)
            async with get_user_db_context(session) as user_db:
                get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)
                async with get_user_manager_context(user_db) as user_manager:
                    user = await create_user(
                        user_manager=user_manager,
                        user_create=instance
                    )
                    if logger:
                        logger.warning(f"User created {user} from scrypt")
    except UserAlreadyExists:
        if logger:
            logger.error(f"User {instance.email} already exists")
        raise
    return user
