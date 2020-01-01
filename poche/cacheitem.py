from dataclasses import dataclass
from datetime import datetime
from typing import Any
from typing import Optional


@dataclass
class Cacheitem:
    expiration: Optional[datetime]
    value: Any

    def __repr__(self):
        return f"poche.Cacheitem({repr(self.expiration)}, {repr(self.value)})"

    def __eq__(self, other: object) -> bool:
        return self.value == getattr(other, "value", other)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: object) -> bool:
        return self.value < getattr(other, "value", other)

    def __gt__(self, other: object) -> bool:
        return self.value > getattr(other, "value", other)

    def __le__(self, other: object) -> bool:
        return self.value <= getattr(other, "value", other)

    def __ge__(self, other: object) -> bool:
        return self.value >= getattr(other, "value", other)
