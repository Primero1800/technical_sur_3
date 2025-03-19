import time
from typing import TYPE_CHECKING

from celery_home.config import app_celery

if TYPE_CHECKING:
    from app1.scripts.scrypt_schemas.email import CustomMessageSchema


@app_celery.task(name="task_send_mail")
async def task_send_mail(
        schema: "CustomMessageSchema",
) -> bool:
    from app1.scripts.mail_sender.utils import send_mail
    return await send_mail(schema=schema)


@app_celery.task(name="task_test_celery")
def test_celery() -> bool:
    for i in range(10):
        print(10-i)
        time.sleep(1)
    return True
