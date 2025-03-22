from datetime import datetime
import pytz

from app1.core.settings import settings


def convert_time(utc_time: datetime | str):
    if isinstance(utc_time, str):
        utc_time = datetime.fromisoformat(utc_time)
        utc_time = utc_time.replace(tzinfo=pytz.UTC)

    local_time = utc_time.astimezone(pytz.timezone(settings.app.APP_TIMEZONE))
    return local_time.isoformat()

