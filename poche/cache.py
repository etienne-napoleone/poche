from collections import UserDict
from typing import Any
from typing import Hashable


class Cache(UserDict):
    def getset(self, key: Hashable, item: Any) -> Any:
        value = self.data.get(key)
        self.data[key] = item
        return value
