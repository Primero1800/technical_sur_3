import asyncio
import logging
import time
from typing import TYPE_CHECKING

from celery.exceptions import MaxRetriesExceededError

from celery_home.config import app_celery

if TYPE_CHECKING:
    from app1.scripts.scrypt_schemas.email import CustomMessageSchema


logger = logging.getLogger(__name__)


@app_celery.task(bind=True, name="task_send_mail")
def task_send_mail(
        self,
        schema: dict,
) -> dict:
    meta = {
        'app_name': '3_sur_app1',
        'task_name': self.name,
        'args': tuple(),
        'kwargs': schema,
    }
    self.update_state(meta={'task_name': self.name})
    from app1.scripts.scrypt_schemas.email import CustomMessageSchema
    schema = CustomMessageSchema(**schema)
    from app1.scripts.mail_sender.utils import send_mail
    result: bool = False

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            result = asyncio.run(send_mail(schema))
        else:
            result = loop.run_until_complete(send_mail(schema))
        if not result:
            raise self.retry(countdown=5, max_retries=3)
    except MaxRetriesExceededError as exc:
        logger.error(f'Task {self.name!r} error: {exc}')
    return {
        "meta": meta,
        "returned_value": result
    }


@app_celery.task(bind=True, name="task_test_celery")
def test_celery(self) -> dict:
    meta = {
        'app_name': '3_sur_app1',
        'task_name': self.name,
        'args': tuple(),
        'kwargs': dict(),
    }
    for i in range(10):
        print(10 - i)
        time.sleep(1)

    result = [12, True]
    return {
        "meta": meta,
        "returned_value": result
    }
