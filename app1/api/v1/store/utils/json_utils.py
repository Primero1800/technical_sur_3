import json
import logging
import os
import shutil
from datetime import datetime
from typing import Dict, Any

from app1.scripts.convert_dates_back import convert_dates

logger = logging.getLogger(__name__)


async def import_data_to_json(
    data: Dict,
    path: str,
    cleaning: bool = False,
) -> bool:
    directory = path

    if os.path.exists(directory):
        # Очищаем директорию, если она существует
        if cleaning:
            logger.info(f"Cleaning folder: {directory}")
            shutil.rmtree(directory)
    else:
        # Создаем директорию, если она не существует
        logger.info(f"Creating folder: {directory}")
        os.makedirs(directory, exist_ok=True)

    # Путь к файлу для записи
    file_path = os.path.join(directory, 'data.json')

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(
            data, json_file,
            ensure_ascii=False, indent=4,
            default=json_datetime_serializer,
        )
    logger.info(f"Data successfully written to {file_path}")

    return True


async def export_data_from_json(
        path: str
) -> Dict:
    directory = path
    file_path = os.path.join(directory, 'data.json')

    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(
            json_file,
        )
    convert_dates(data)
    logger.info(f"Data has successfully read from {file_path}")
    return data


def json_datetime_serializer(
    obj: Any,
    timezone: str | None = None
):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Преобразуем datetime в строку ISO 8601
    raise TypeError(f"Type {type(obj)} not serializable")

