from datetime import datetime
from typing import Any, Optional


class Item:
    """Cache item

    Holde the item value and expiration.

    Args:
        value (Any): Item value.
        expiration (Optional[datetime]): Item expiration.
    """

    def __init__(self, value: Any, expiration: Optional[datetime]) -> None:
        self.value = value
        self.expiration = expiration

    def __repr__(self) -> str:
        return "Item({}, {})".format(
            f'"{self.value}"' if isinstance(self.value, str) else self.value,
            self.expiration,
        )

    def is_expired(self) -> bool:
        """Check if the item is expired.

        Returns:
            bool: Is expired.
        """
        if self.expiration and self.expiration <= datetime.now():
            return True
        return False
