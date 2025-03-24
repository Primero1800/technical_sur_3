from datetime import timedelta

from celery_home.settings import settings as _settings

broker_url = _settings.celery.CELERY_BROKER_URL
result_backend = _settings.celery.CELERY_BROKER_BACKEND

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

broker_connection_retry_on_startup = True

timezone = _settings.celery.APP_TIMEZONE

result_expires = timedelta(days=_settings.celery.CELERY_RESULT_EXPIRES_DAYS)
# result_expires = timedelta(hours=settings.celery.CELERY_RESULT_EXPIRES_HOURS)


