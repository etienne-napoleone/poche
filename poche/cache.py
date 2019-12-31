from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple


class Cache:
    _store: Dict[str, Tuple[Optional[datetime], Any]] = {}

    @staticmethod
    def set(
        key: str, value: Any, ttl: Optional[int] = None, override: bool = True
    ) -> None:
        if not isinstance(key, str):
            raise TypeError("The key should be of string type.")
        if override:
            Cache._store[key] = (
                Cache._get_expiration_dt(ttl) if ttl else None,
                value,
            )
        else:
            Cache._store.setdefault(
                key, (Cache._get_expiration_dt(ttl) if ttl else None, value)
            )

    @staticmethod
    def get(key: str) -> Any:
        if not isinstance(key, str):
            raise TypeError("The key should be of string type.")
        value_tuple = Cache._store.get(key)
        if not value_tuple:
            raise KeyError(key)
        elif isinstance(value_tuple[0], datetime):
            if value_tuple[0] > datetime.now():
                return value_tuple[1]
            else:
                del Cache._store[key]
                raise KeyError(key)
        else:
            return value_tuple[1]

    @staticmethod
    def flush() -> None:
        Cache._store = {}

    @staticmethod
    def _get_expiration_dt(ttl: int) -> datetime:
        return datetime.now() + timedelta(seconds=ttl)
