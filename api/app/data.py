from dataclasses import dataclass
from typing import List

@dataclass
class Street:
    name: str
    city_name: str

@dataclass
class ActivityData:
    id: str
    completed_streets: int
    date: str
    distance: str
    streets: List[Street]