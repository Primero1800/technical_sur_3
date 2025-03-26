import logging
import os
import shutil

from fastapi import UploadFile

logger = logging.getLogger(__name__)


async def save_image(
    image_object: UploadFile,
    folder: str,
    path: str,
    name: str = 'logo',
    cleaning: bool = True
):
    directory = f"{path}/{folder}"

    if cleaning and os.path.exists(directory):                                          # Очищаем директорию, если она существует
        logger.info(f"Cleaning folder: {directory}")
        shutil.rmtree(directory)

    os.makedirs(directory, exist_ok=True)                                               # Создаем директорию, если она не существует
    logger.info(f"Creating folder: {directory}")

    extension = os.path.splitext(image_object.filename)[1]
    new_file_name = f"{name}{extension}"
    file_path = os.path.join(directory, new_file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image_object.file, buffer)
        logger.info(f"Writing file: {image_object.file}")

    return file_path
