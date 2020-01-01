from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import Hashable
from typing import ItemsView
from typing import KeysView
from typing import Optional
from typing import Union
from typing import ValuesView

from poche.cacheitem import Cacheitem


class Cache:
    def __init__(
        self, default_ttl: Optional[Union[int, datetime]] = None
    ) -> None:
        self.default_ttl = default_ttl
        self._store: Dict[Hashable, Cacheitem] = {}

    def __len__(self) -> int:
        return len(self._store)

    def __getitem__(self, key: Hashable) -> Cacheitem:
        return self._store[key]

    def __setitem__(self, key: Hashable, value: Cacheitem) -> None:
        if not isinstance(value, Cacheitem):
            raise TypeError(f"Expected Cacheitem, got {type(value)}.")
        self._store[key] = value

    def __delitem__(self, key: Hashable) -> None:
        del self._store[key]

    def __contains__(self, key: Hashable) -> bool:
        return key in self._store

    def set(
        self,
        key: Hashable,
        value: Any,
        ttl: Optional[Union[int, datetime]] = None,
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

    def gos(self, key: Hashable, value: Any, ttl: Optional[int] = None) -> Any:
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

    def _get_expiration(
        self, ttl: Optional[Union[int, datetime]]
    ) -> Optional[datetime]:
        if ttl:
            return (
                (datetime.now() + timedelta(seconds=ttl))
                if isinstance(ttl, int)
                else ttl
            )
        elif self.default_ttl:
            return (
                (datetime.now() + timedelta(seconds=self.default_ttl))
                if isinstance(self.default_ttl, int)
                else self.default_ttl
            )
        else:
            return None
