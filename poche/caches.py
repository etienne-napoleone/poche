from datetime import datetime, timedelta
from typing import Any, Dict, Hashable, Optional, Union

from .items import Item


class Cache:
    """Cache with expiration mechanisme.

    When a default ttl is given, all items set without a ttl will get
    an expiration based on it. Items with a ttl are expired on access. This is
    why only single item access methods are implemented.

    Args:
        ttl (Optional[Union[int, timedelta]], optional): ttl. Defaults to None.

    Raises:
        TypeError: Raised when ttl is not of the correct type.
    """

    def __init__(self, ttl: Optional[Union[int, timedelta]] = None) -> None:

        self._items: Dict[Hashable, Item] = {}
        if ttl is None or isinstance(ttl, timedelta):
            self.ttl = ttl
        elif isinstance(ttl, int) and not isinstance(ttl, bool):
            self.ttl = timedelta(seconds=ttl)
        else:
            raise TypeError("ttl should be of type Optional[Union[int, timedelta]]")

    def __repr__(self) -> str:
        return f"Cache({self.ttl})"

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
        """Get the expiration datetime from a ttl.

        Args:
            ttl (Optional[Union[int, timedelta, datetime]]): Time to live.

        Raises:
            TypeError: Raised when ttl is not of the correct type.

        Returns:
            Optional[datetime]: Expiration.
        """
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
        """Get a value from the cache.

        On call, check if the item at key `key` has an expiration.
        If the item is expired, delete it.
        Then try to get the item at `key` and return the value or
        None if absent.

        Args:
            key (Hashable): Cache key.

        Returns:
            Optional[Any]: Value of the item in cache.
        """
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
        """Set a value in the cache.

        The ttl is optional and will default to the cache ttl if present.

        Args:
            key (Hashable): Cache key.
            value (Any): Value to cache.
            ttl (Optional[Union[int, timedelta, datetime]]): ttl. Defaults to None.
        """
        self._items[key] = Item(
            value=value, expiration=self._get_expiration_from_ttl(ttl)
        )

    def getset(
        self,
        key: Hashable,
        value: Any,
        ttl: Optional[Union[int, timedelta, datetime]] = None,
    ) -> Optional[Any]:
        """Get a value from the cache, then set it.

        Args:
            key (Hashable): Cache key.
            value (Any): Value to cache.
            ttl (Optional[Union[int, timedelta, datetime]]): ttl. Defaults to None.

        Returns:
            Optional[Any]: Value of the item in cache.
        """
        old_value = self.get(key)
        self.set(key, value=value, ttl=ttl)
        return old_value

    def flush(self) -> None:
        """Flush the cache content"""
        self._items = {}
