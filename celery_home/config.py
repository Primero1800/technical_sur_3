from celery import Celery

from celery_home.beat_home.beat_schedule import schedule as beat_schedule
from celery_home.settings import settings

# command
#  celery -A celery_home.config.app_celery worker --loglevel=info | celery -A celery_home.config.app_celery flower | celery -A celery_home.config.app_celery beat  --loglevel=info
app_celery = Celery(settings.celery.APP_NAME)


app_celery.config_from_object("celery_home.file_config")


app_celery.autodiscover_tasks(
    packages=["app1.api.v1.celery_tasks",]
)


app_celery.conf.beat_schedule = beat_schedule
