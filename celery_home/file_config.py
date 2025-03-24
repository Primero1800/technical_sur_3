from datetime import timedelta

from celery_home.crontabs import Crontabs
from celery_home.settings import settings

broker_url = settings.celery.CELERY_BROKER_URL
result_backend = settings.celery.CELERY_BROKER_BACKEND

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

broker_connection_retry_on_startup = True

timezone = settings.celery.APP_TIMEZONE

result_expires = timedelta(days=settings.celery.CELERY_RESULT_EXPIRES_DAYS)
# result_expires = timedelta(hours=settings.celery.CELERY_RESULT_EXPIRES_HOURS)


beat_schedule = {
    # 'run-every-minute': {
    #     'task': 'task_beat_test_every_minute',
    #     'schedule': Crontabs.every_minute,
    #     'args': (100, )
    # },
    'run-every-2-minutes': {
        'task': 'task_beat_test_every_minute',
        'schedule': Crontabs.every_2_minutes,
        'args': (200,)
    },
    'run-every-hour': {
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
