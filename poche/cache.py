from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import Hashable
from typing import ItemsView
from typing import KeysView
from typing import Optional
from typing import ValuesView

from poche.cacheitem import Cacheitem


class Cache:
    def __init__(self, default_ttl: Optional[int] = None) -> None:
        self.default_ttl = default_ttl
        self._store: Dict[Hashable, Cacheitem] = {}

    def __len__(self) -> int:
        return len(self._store)

    def __getitem__(self, key: Hashable) -> Cacheitem:
        return self._store[key]

    def set(
        self, key: Hashable, value: Any, ttl: Optional[int] = None,
    ) -> None:
        self._store[key] = Cacheitem(self._get_expiration(ttl), value)

    def get(self, key: Hashable) -> Any:
        item = self._store[key]
        if (
            isinstance(item.expiration, datetime)
            and item.expiration < datetime.now()
        ):
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

    def keys(self) -> KeysView[Hashable]:
        return self._store.keys()

    def values(self) -> ValuesView[Any]:
        return self._store.values()

    def items(self) -> ItemsView[Hashable, Cacheitem]:
        return self._store.items()

    def flush(self) -> None:
        self._store.clear()

    def _get_expiration(self, ttl: Optional[int]) -> Optional[datetime]:
        if ttl:
            return datetime.now() + timedelta(seconds=ttl)
        elif self.default_ttl:
            return datetime.now() + timedelta(seconds=self.default_ttl)
        else:
            return None
