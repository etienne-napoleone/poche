from collections import UserDict
from typing import Any
from typing import Hashable
from typing import Optional


class Cache(UserDict):
    def getset(self, key: Hashable, value: Any) -> Optional[Any]:
        """Get an item from the cache and set the value

        Args:
            key (Hashable): cache key
            value (Any): cached value

        Returns:
            Optional[Any]: previous cached value if any
        """
        old_value = self.data.get(key)
        self.data[key] = value
        return old_value
