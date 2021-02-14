from collections import UserDict
from typing import Any
from typing import Hashable
from typing import Optional


class Cache(UserDict):
    def getset(self, key: Hashable, item: Any) -> Optional[Any]:
        """Get an item from the cache and set the value

        Args:
            key (Hashable): cache key
            item (Any): cached value

        Returns:
            Optional[Any]: previous cached value if any
        """
        value = self.data.get(key)
        self.data[key] = item
        return value
