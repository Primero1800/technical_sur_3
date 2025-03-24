from celery import Celery

from celery_home.crontabs import Crontabs
from celery_home.settings import settings

# command
#  celery -A celery_home.config.app_celery worker --loglevel=info | celery -A celery_home.config.app_celery flower | celery -A celery_home.config.app_celery beat  --loglevel=info
app_celery = Celery(settings.celery.APP_NAME)


app_celery.config_from_object("celery_home.file_config")


app_celery.autodiscover_tasks(
    packages=["app1.api.v1.celery_tasks",]
)


app_celery.conf.beat_schedule = {
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