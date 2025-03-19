import asyncio
import time
from typing import TYPE_CHECKING

from celery_home.config import app_celery

if TYPE_CHECKING:
    from app1.scripts.scrypt_schemas.email import CustomMessageSchema


@app_celery.task(name="task_send_mail")
def task_send_mail(
        schema: dict,
) -> bool:
    from app1.scripts.scrypt_schemas.email import CustomMessageSchema
    schema = CustomMessageSchema(**schema)
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    from app1.scripts.mail_sender.utils import send_mail
    loop = asyncio.get_event_loop()
    if loop.is_running():
        result = asyncio.run(send_mail(schema))
    else:
        result = loop.run_until_complete(send_mail(schema))
    return result


@app_celery.task(name="task_test_celery")
def test_celery() -> bool:
    for i in range(10):
        print(10-i)
        time.sleep(1)
    return True
