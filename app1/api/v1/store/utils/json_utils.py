import json
import logging
import os
import shutil
from datetime import datetime
from typing import Dict


logger = logging.getLogger(__name__)


async def import_data_to_json(
    data: Dict,
    path: str,
    cleaning: bool = False
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

    # Запись данных в json файл
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(
            data, json_file,
            ensure_ascii=False, indent=4,
            default=json_datetime_serializer,
        )
    logger.info(f"Data successfully written to {file_path}")

    return True


def json_datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Преобразуем datetime в строку ISO 8601
    raise TypeError(f"Type {type(obj)} not serializable")
