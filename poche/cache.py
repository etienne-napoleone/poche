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
        Cache._raise_if_not_str(key)
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
        Cache._raise_if_not_str(key)
        value = Cache._store[key]
        if isinstance(value[0], datetime) and value[0] < datetime.now():
            del Cache._store[key]
            raise KeyError
        else:
            return value[1]

    @staticmethod
    def flush() -> None:
        Cache._store.clear()

    @staticmethod
    def _get_expiration_dt(ttl: int) -> datetime:
        return datetime.now() + timedelta(seconds=ttl)

    @staticmethod
    def _raise_if_not_str(value: Any) -> None:
        if not isinstance(value, str):
            raise TypeError
