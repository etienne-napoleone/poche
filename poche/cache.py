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
    ):
        if override:
            Cache._store[key] = (
                Cache.get_expiration(ttl) if ttl else None,
                value,
            )
        else:
            Cache._store.setdefault(
                key, (Cache.get_expiration(ttl) if ttl else None, value)
            )

    @staticmethod
    def get(key: str) -> Any:
        value_tuple = Cache._store.get(key)
        print(value_tuple)
        if not value_tuple:
            return None
        elif isinstance(value_tuple[0], datetime):
            if value_tuple[0] > datetime.now():
                return value_tuple[1]
            else:
                del Cache._store[key]
                return None
        else:
            print("no ttl")
            return value_tuple[1]

    @staticmethod
    def get_expiration(ttl: int) -> datetime:
        return datetime.now() + timedelta(seconds=ttl)
