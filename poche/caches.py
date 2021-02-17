from datetime import datetime, timedelta
from typing import Any, Dict, Hashable, Optional, Union

from .items import Item


class Cache:
    def __init__(self, ttl: Optional[Union[int, timedelta]] = None) -> None:
        self._items: Dict[Hashable, Item] = {}
        if ttl is None or isinstance(ttl, timedelta):
            self.ttl = ttl
        elif isinstance(ttl, int) and not isinstance(ttl, bool):
            self.ttl = timedelta(seconds=ttl)
        else:
            raise TypeError("ttl should be of type Optional[Union[int, timedelta]]")

    def __delitem__(self, key: Hashable) -> None:
        del self._items[key]

    def __getitem__(self, key: Hashable) -> Any:
        value = self.get(key)
        if not value:
            raise KeyError
        return value

    def _get_expiration_from_ttl(
        self, ttl: Optional[Union[int, timedelta, datetime]]
    ) -> Optional[datetime]:
        if ttl is None:
            return (datetime.now() + self.ttl) if self.ttl else None
        elif isinstance(ttl, int) and not isinstance(ttl, bool):
            return datetime.now() + timedelta(seconds=ttl)
        elif isinstance(ttl, timedelta):
            return datetime.now() + ttl
        elif isinstance(ttl, datetime):
            return ttl
        else:
            raise TypeError("ttl should be of type Optional[Union[int, timedelta]]")

    def get(self, key: Hashable) -> Optional[Any]:
        item = self._items.get(key)
        if not item:
            return None
        elif item and item.is_expired():
            del self._items[key]
            return None
        return item.value

    def set(
        self,
        key: Hashable,
        value: Any,
        ttl: Optional[Union[int, timedelta, datetime]] = None,
    ) -> None:
        self._items[key] = Item(
            value=value, expiration=self._get_expiration_from_ttl(ttl)
        )

    def getset(
        self,
        key: Hashable,
        value: Any,
        ttl: Optional[Union[int, timedelta, datetime]] = None,
    ) -> Optional[Any]:
        old_value = self.get(key)
        self.set(key, value=value, ttl=ttl)
        return old_value

    def flush(self) -> None:
        self._items = {}
