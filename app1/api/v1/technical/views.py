import logging
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app1.core.auth.fastapi_users_config import current_superuser
from app1.core.config import DBConfigurer
from app1.exceptions import CustomException

from . import crud


logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/view_data", dependencies=[Depends(current_superuser)])
async def export_data(
    session: AsyncSession = Depends(DBConfigurer.session_getter)
):

    data = await crud.get_all_data(
        session=session
    )
    return data


@router.get("/export_data", dependencies=[Depends(current_superuser)])
async def export_data(
    session: AsyncSession = Depends(DBConfigurer.session_getter)
):
    try:
        result = await crud.get_all_data_and_write_to_json(
            session=session
        )
        if result:
            return {"status": "Data was successfully exported to json"}
    except CustomException as exc:
        return ORJSONResponse(
            status_code=exc.status_code,
            content={
                "message": "Handled by Endpoint ExceptionHandler",
                "detail": exc.msg,
            }
        )


@router.post(
    "/import_data",
    dependencies=[Depends(current_superuser)]
)
async def import_data(
        data: Dict[str, List[Dict]],
        session: AsyncSession = Depends(DBConfigurer.session_getter)
):

    try:
        return await crud.import_data_from_json(
            data=data,
            session=session,
        )
    except CustomException as exc:
        return ORJSONResponse(
            status_code=exc.status_code,
            content={
                "message": "Handled by Endpoint ExceptionHandler",
                "detail": {exc.msg},
            }
        )



#
#
# # Эндпоинт для загрузки данных из JSON в БД
# @app.post("/import_data", dependencies=[Depends(current_superuser)])
# async def import_data(data: Dict[str, List[Dict]], session: AsyncSession = Depends(AsyncSessionLocal)):
#     async with session.begin():
#         for model_name, records in data.items():
#             model = get_model_by_name(model_name)  # Функция для получения модели по имени
#             for record in records:
#                 obj = model(**record)
#                 session.add(obj)
#     await session.commit()
#     return {"status": "Data imported successfully"}
#
#
# # Опциональный эндпоинт для вывода JSON на экран
# @app.get("/show_data", dependencies=[Depends(current_superuser)])
# async def show_data(session: AsyncSession = Depends(AsyncSessionLocal)):
#     data = await export_data(session)  # Используем тот же метод, что и для экспорта
#     return data
#
#
# # Функция для получения модели по имени
# def get_model_by_name(model_name: str):
#     if model_name == "YourModel1":
#         return YourModel1
#     elif model_name == "YourModel2":
#         return YourModel2
#     # Добавьте другие модели
#     raise HTTPException(status_code=400, detail="Model not found")