from datetime import datetime
import pytz

from app1.core.settings import settings


def convert_time(utc_time: datetime | str):
    if isinstance(utc_time, str):
        utc_time = datetime.fromisoformat(utc_time)
        utc_time = utc_time.replace(tzinfo=pytz.UTC)

    local_time = utc_time.astimezone(pytz.timezone(settings.app.APP_TIMEZONE))
    return local_time.isoformat()


def convert_naive_time_to_aware(naive_time: datetime | str):
    local_timezone = pytz.timezone(settings.app.APP_TIMEZONE)
    return naive_time.replace(tzinfo=local_timezone)
