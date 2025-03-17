import asyncio
import contextlib
from logging import Logger
from typing import Sequence
from sqlalchemy import select, Result


from app1.core.models import AccessToken


async def delete_expired_tokens_from_db(
        logger: Logger = None,
) -> Sequence[AccessToken]:
    # from app1.core.auth.access_token import get_access_token_db
    from app1.core.config import DBConfigurer

    async with DBConfigurer.Session() as session:

        # get_access_token_db_context = contextlib.asynccontextmanager(get_access_token_db)
        # async with get_access_token_db_context(session) as access_token_db:

            stmt = select(AccessToken).order_by(AccessToken.user_id)
            result: Result = await session.execute(stmt)

            result_to_return = result.scalars().all()
            print("QQQ", result_to_return)
            return result_to_return


if __name__ == "__main__":
    print("Scrypt starting")
    asyncio.run(delete_expired_tokens_from_db())
