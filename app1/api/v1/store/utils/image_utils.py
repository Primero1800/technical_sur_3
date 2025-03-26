import logging
import os
import shutil

from fastapi import UploadFile

logger = logging.getLogger(__name__)


async def save_image(
    instance_id: int,
    image_object: UploadFile,
    folder: str
):
    directory = f"{folder}/{instance_id}"
    os.makedirs(directory, exist_ok=True)                                               # Создаем директорию, если она не существует
    logger.info(f"Creating folder: {directory}")
    file_path = os.path.join(directory, image_object.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image_object.file, buffer)
        logger.info(f"Writing file: {image_object.file}")

    return file_path
