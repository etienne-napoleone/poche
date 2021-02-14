from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Optional
from typing import Union

from .utils import timedelta_to_datetime


class TTLItem:
    def __init__(
        self, value: Any, ttl: Optional[Union[datetime, timedelta]] = None
    ) -> None:
        self.value = value
        if not ttl or isinstance(ttl, datetime):
            self.ttl = ttl
        else:
            self.ttl = timedelta_to_datetime(ttl)
