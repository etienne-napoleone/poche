from typing import Any
from typing import Dict


class Cache:
    _store: Dict[str, Any] = {}

    @staticmethod
    def set(key: str, value: Any, override: bool = True):
        if override:
            Cache._store[key] = value
        else:
            Cache._store.setdefault(key, value)

    @staticmethod
    def get(key: str) -> Any:
        return Cache._store[key]
