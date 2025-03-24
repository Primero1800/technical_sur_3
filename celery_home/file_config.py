from datetime import timedelta

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
