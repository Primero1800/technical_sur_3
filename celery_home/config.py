from celery import Celery


# command
#  celery -A celery_home.config.app_celery worker --loglevel=info | celery -A celery_home.config.app_celery flower | celery -A celery_home.config.app_celery beat  --loglevel=info
app_celery = Celery(__name__)


app_celery.config_from_object("celery_home.file_config")


app_celery.autodiscover_tasks(
    packages=["app1.api.v1.celery_tasks",]
)


