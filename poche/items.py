from datetime import datetime
from typing import Any, Optional


class Item:
    def __init__(self, value: Any, expiration: Optional[datetime]) -> None:
        self.value = value
        self.expiration = expiration

    def is_expired(self) -> bool:
        if self.expiration and self.expiration <= datetime.now():
            return True
        return False
