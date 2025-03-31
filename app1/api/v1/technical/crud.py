import logging

from fastapi import status
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app1.core.models import __all__ as all_models_names
from app1.core.models import *
from app1.exceptions import CustomException

abstract_models = [
    "Base",
]

logger = logging.getLogger(__name__)


async def get_all_data(
    session: AsyncSession
):
    all_models_classes = [globals()[name] for name in all_models_names if name not in abstract_models]

    data = {}
    try:
        for model in all_models_classes:
            stmt = select(model)
            results: Result = await session.execute(stmt)
            data[model.__name__] = [result.to_dict() for result in results.scalars().all()]
    except (IntegrityError, Exception) as exc:
        logger.error("Error while getting data from db", exc_info=exc)
        raise CustomException(
            msg="Error while getting data from db",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return data
