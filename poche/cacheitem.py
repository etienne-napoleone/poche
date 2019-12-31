from dataclasses import dataclass
from datetime import datetime
from typing import Any
from typing import Optional


@dataclass
class Cacheitem:
    expire: Optional[datetime]
    value: Any
