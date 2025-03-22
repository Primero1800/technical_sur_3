from datetime import timedelta
from celery import Celery

from celery_home.settings import settings
from .crontabs import Crontabs


# command
#  celery -A celery_home.config.app_celery worker --loglevel=info | celery -A celery_home.config.app_celery flower | celery -A celery_home.config.app_celery beat  --loglevel=info
app_celery = Celery(__name__)

app_celery.autodiscover_tasks(
    packages=["app1.api.v1.celery_tasks",]
)

app_celery.conf.broker_url = settings.celery.CELERY_BROKER_URL
app_celery.conf.result_backend = settings.celery.CELERY_BROKER_BACKEND

# app_celery.conf.result_expires = timedelta(days=settings.celery.CELERY_RESULT_EXPIRES_DAYS)
app_celery.conf.result_expires = timedelta(hours=settings.celery.CELERY_RESULT_EXPIRES_HOURS)


app_celery.conf.beat_schedule = {
    # 'run-every-minute': {
    #     'task': 'task_beat_test_every_minute',
    #     'schedule': Crontabs.every_minute,
    #     'args': (100, )
    # },
    'run-every-2-minutes': {
        'task': 'task_beat_test_every_minute',
        'schedule': Crontabs.every_hour,
        'args': (6000,)
    },
    # 'run-every-10-minutes': {
    #     'task': 'task_beat_test_every_minute',
    #     'schedule': Crontabs.every_10_minutes,
    #     'args': (1000,)
    # },
    # 'run-every-day': {
    #     'task': None,
    #     'schedule': Crontabs.every_day,
    #     'args': (10, 20)
    # },
}

