import asyncio
import logging

from app1.core.settings import settings
from app1.api.v1.users.schemas import UserCreate
from app1.scripts.create_user import create_user_straight

logger = logging.getLogger(__name__)


# PYTHONPATH=.. python scripts/create_superuser.py
async def create_superuser(
        email: str = settings.superuser.SUPERUSER_EMAIL,
        password: str = settings.superuser.SUPERUSER_PASSWORD,
        is_active: bool = settings.superuser.SUPERUSER_IS_ACTIVE,
        is_verified: bool = settings.superuser.SUPERUSER_IS_VERIFIED,
        is_superuser: bool = settings.superuser.SUPERUSER_IS_SUPERUSER,
        display_name: str = 'Superuser'
):
    user_create = UserCreate(
        email=email,
        password=password,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
        display_name=display_name,
    )
    return await create_user_straight(
        instance=user_create,
        logger=logger,
    )


if __name__ == "__main__":

    logger.info('Creating SUPERUSER. You can change all the parameters in .env-files.')
    asyncio.run(create_superuser())
