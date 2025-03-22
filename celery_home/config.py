from datetime import timedelta

from celery import Celery
from flower.app import Flower

from celery_home.settings import settings


# command
#  celery -A celery_home.config.app_celery worker --loglevel=info | celery -A celery_home.config.app_celery flower
app_celery = Celery(__name__)

app_celery.autodiscover_tasks(
    packages=["app1.api.v1.celery_tasks",]
)

app_flower = Flower()

app_celery.conf.broker_url = settings.celery.CELERY_BROKER_URL
app_celery.conf.result_backend = settings.celery.CELERY_BROKER_BACKEND

app_celery.conf.result_expires = timedelta(days=settings.celery.CELERY_RESULT_EXPIRES_DAYS)
