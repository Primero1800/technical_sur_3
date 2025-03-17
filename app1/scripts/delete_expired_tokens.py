import asyncio
import logging
from datetime import timedelta
from typing import Sequence
from sqlalchemy import select, Result, func, delete

from app1.core.config import DBConfigurer
from app1.core.models import AccessToken


app_logger = logging.getLogger(__name__)


# PYTHONPATH=.. python scripts/delete_expired_tokens.py
async def delete_expired_tokens_from_db(
        logger: logging.Logger = app_logger,
) -> Sequence[AccessToken]:

    logger.info("SCRIPT delete_expired_tokens_from_db STARTED.")
    from app1.core.settings import settings

    async with DBConfigurer.Session() as session:

        expired_frontier = func.now() - timedelta(
            seconds=settings.access_token.ACCESS_TOKEN_LIFETIME
        )
        stmt = select(AccessToken).where(AccessToken.created_at < expired_frontier)
        result: Result = await session.execute(stmt)
        result_to_return = result.scalars().all()
        logger.info(f"Expired tokens to delete: {len(result_to_return)}")

        stmt = delete(AccessToken).where(AccessToken.created_at < expired_frontier)
        await session.execute(stmt)
        logger.info(f"Expired tokens to deleted")

        return result_to_return


if __name__ == "__main__":
    result = asyncio.run(delete_expired_tokens_from_db())

    print(result)
