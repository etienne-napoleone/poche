from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import Hashable
from typing import Optional

from poche.cacheitem import Cacheitem


class Cache:
    def __init__(self, default_ttl: Optional[int] = None) -> None:
        self.default_ttl = default_ttl
        self._store: Dict[Hashable, Cacheitem] = {}

    def set(
        self, key: Hashable, value: Any, ttl: Optional[int] = None,
    ) -> None:
        self._store[key] = Cacheitem(self._get_expiration(ttl), value)

    def get(self, key: Hashable) -> Any:
        item = self._store[key]
        if isinstance(item.expire, datetime) and item.expire < datetime.now():
            del self._store[key]
            raise KeyError
        else:
            return item.value

    def get_or_set(
        self, key: Hashable, value: Any, ttl: Optional[int] = None
    ) -> Any:
        try:
            return self.get(key)
        except KeyError:
            self.set(key, value, ttl)
            return value

    def delete(self, key: Hashable) -> None:
        del self._store[key]

    def flush(self) -> None:
        self._store.clear()

    def _get_expiration(self, ttl: Optional[int]) -> Optional[datetime]:
        if ttl:
            return datetime.now() + timedelta(seconds=ttl)
        elif self.default_ttl:
            return datetime.now() + timedelta(seconds=self.default_ttl)
        else:
            return None
