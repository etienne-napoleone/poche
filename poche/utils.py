from datetime import datetime
from datetime import timedelta


def timedelta_to_datetime(delta: timedelta) -> datetime:
    return datetime.now() + delta
