from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import Hashable
from typing import Optional
from typing import Tuple


class Cache:
    _store: Dict[Hashable, Tuple[Optional[datetime], Any]] = {}

    @staticmethod
    def set(
        key: Hashable,
        value: Any,
        ttl: Optional[int] = None,
        override: bool = True,
    ) -> None:
        if not override and Cache._store.get(key):
            pass
        else:
            Cache._store[key] = (
                Cache._get_expiration_dt(ttl) if ttl else None,
                value,
            )

    @staticmethod
    def get(key: Hashable) -> Any:
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
