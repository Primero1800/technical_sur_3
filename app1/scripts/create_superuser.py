import asyncio
import contextlib
import logging

from app1.core.config import (
    DBConfigurer,
    FastAPIUsersConfigurer,
)
from app1.core.authentication.user_manager import UserManager
from app1.core.settings import settings

from app1.api.v1.schemas.user import UserCreate
from fastapi_users.exceptions import UserAlreadyExists

from app1.core.models import User

logger = logging.getLogger(__name__)


async def create_user(
        user_manager: UserManager,
        user_create: UserCreate,
) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=False,
    )
    return user


# PYTHONPATH=.. python scripts/create_superuser.py
async def create_superuser(
        email: str = settings.superuser.SUPERUSER_EMAIL,
        password: str = settings.superuser.SUPERUSER_PASSWORD,
        is_active: bool = settings.superuser.SUPERUSER_IS_ACTIVE,
        is_verified: bool = settings.superuser.SUPERUSER_IS_VERIFIED,
        is_superuser: bool = settings.superuser.SUPERUSER_IS_SUPERUSER,
):
        user_create = UserCreate(
            email=email,
            password=password,
            is_active=is_active,
            is_superuser=is_superuser,
            is_verified=is_verified,
        )
        try:
            async with DBConfigurer.Session() as session:
                get_user_db_context = contextlib.asynccontextmanager(FastAPIUsersConfigurer.get_user_db)
                async with get_user_db_context(session) as user_db:
                    get_user_manager_context = contextlib.asynccontextmanager(FastAPIUsersConfigurer.get_user_manager)
                    async with get_user_manager_context(user_db) as user_manager:
                        user = await create_user(
                            user_manager=user_manager,
                            user_create=user_create
                        )
                        logger.warning(f"User created {user} from scrypt")
        except UserAlreadyExists:
            logger.error(f"User {email} already exists")
            raise
        return user


if __name__ == "__main__":
    # email: str = input("Superuser. Input valid email: ")
    # password: str = input("Superuser. Input valid password: ")
    # flag: str = input("Superuser. Input 'true' to create superuser: ")
    # is_superuser: bool = flag == 'true'
    logger.info('Creating SUPERUSER. You can change all the parameters in .env-files.')
    asyncio.run(create_superuser())