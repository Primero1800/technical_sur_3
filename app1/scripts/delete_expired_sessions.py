import asyncio
import logging

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func, Result, delete

from app1.core.config import DBConfigurer
from app1.core.models import Session

app_logger = logging.getLogger(__name__)


async def delete_expired_sessions_from_db(
        logger: logging.Logger = app_logger,
) -> list[Session]:

    logger.info("SCRIPT delete_expired_sessions_from_db STARTED.")
    from app1.core.settings import settings

    async with DBConfigurer.Session() as session:

        stmt = select(Session).where(Session.expired_at < func.now())
        result: Result = await session.execute(stmt)
        result_to_return = result.scalars().all()
        logger.info(f"Expired sessions to delete: {len(result_to_return)}")

        stmt = delete(Session).where(Session.expired_at < func.now())
        await session.execute(stmt)
        await session.commit()
        logger.info(f"Expired sessions to deleted")

        return jsonable_encoder(list(result_to_return))


if __name__ == "__main__":
    result = asyncio.run(delete_expired_sessions_from_db())

    print(result)