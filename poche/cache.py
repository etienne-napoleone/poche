from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import Hashable
from typing import Optional
from typing import Tuple


class Cache:
    def __init__(self):
        self._store: Dict[Hashable, Tuple[Optional[datetime], Any]] = {}

    def set(
        self,
        key: Hashable,
        value: Any,
        ttl: Optional[int] = None,
        override: bool = True,
    ) -> None:
        if not override and self._store.get(key):
            pass
        else:
            self._store[key] = (
                self._get_expiration_dt(ttl) if ttl else None,
                value,
            )

    def get(self, key: Hashable) -> Any:
        value = self._store[key]
        if isinstance(value[0], datetime) and value[0] < datetime.now():
            del self._store[key]
            raise KeyError
        else:
            return value[1]

    def flush(self) -> None:
        self._store.clear()

    def _get_expiration_dt(self, ttl: int) -> datetime:
        return datetime.now() + timedelta(seconds=ttl)
