import logging
from typing import Dict, List

from fastapi import status
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app1.api.v1.store.utils.json_utils import import_data_to_json
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
    all_models_classes = [await get_model_by_name(name) for name in all_models_names if name not in abstract_models]

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


async def get_all_data_and_write_to_json(
    session: AsyncSession
):
    data: Dict = await get_all_data(session=session)

    path: str = f"app1/fixtures"
    try:
        result = await import_data_to_json(
            data=data,
            path=path
        )
    except Exception as exc:
        logger.error("Error while putting data to json file", exc_info=exc)
        raise CustomException(
            msg="Error while putting data to json file",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return result



async def import_data_from_json(
    data: Dict[str, List[Dict]],
    session: AsyncSession,
) -> Dict:
    try:
        for model_name, records in data.items():
            model = await get_model_by_name(model_name)
            for record in records:
                obj = model(**record)
                session.add(obj)
        await session.commit()
    except (IntegrityError, Exception) as exc:
        logger.error("Error while putting data to db", exc_info=exc)
        raise CustomException(
            msg="Error while putting data to db",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return {"status": "Data imported successfully"}


async def get_model_by_name(model_name: str):
    return globals()[model_name]
