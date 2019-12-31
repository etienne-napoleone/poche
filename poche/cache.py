from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import Hashable
from typing import Optional
from typing import Tuple


class Cache:
    def __init__(self, default_ttl: Optional[int] = None) -> None:
        self.default_ttl = default_ttl
        self._store: Dict[Hashable, Tuple[Optional[datetime], Any]] = {}

    def set(
        self, key: Hashable, value: Any, ttl: Optional[int] = None,
    ) -> None:
        self._store[key] = (
            self._get_expiration(ttl),
            value,
        )

    def get(self, key: Hashable) -> Any:
        value = self._store[key]
        if isinstance(value[0], datetime) and value[0] < datetime.now():
            del self._store[key]
            raise KeyError
        else:
            return value[1]

    def get_or_set(
        self, key: Hashable, value: Any, ttl: Optional[int] = None
    ) -> Any:
        try:
            return self.get(key)
        except KeyError:
            self.set(key, value, ttl)
            return value

    def flush(self) -> None:
        self._store.clear()

    def _get_expiration(self, ttl: Optional[int]) -> Optional[datetime]:
        if ttl:
            return datetime.now() + timedelta(seconds=ttl)
        elif self.default_ttl:
            return datetime.now() + timedelta(seconds=self.default_ttl)
        else:
            return None
