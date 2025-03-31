from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app1.core.auth.fastapi_users_config import current_superuser
from app1.core.config import DBConfigurer

from . import crud


router = APIRouter()


@router.get("/view_data", dependencies=[Depends(current_superuser)])
async def export_data(
    session: AsyncSession = Depends(DBConfigurer.session_getter)
):

    data = await crud.get_all_data(
        session=session
    )
    return data


#     async with session.begin():
#         # Получение данных из всех моделей
#         for model in [YourModel1, YourModel2]:  # Замените на ваши модели
#             results = await session.execute(select(model))
#             data[model.__name__] = [result._asdict() for result in results.scalars()]
#
#     return data
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