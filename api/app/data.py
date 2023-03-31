from dataclasses import dataclass
from typing import List, TypedDict

@dataclass
class Street(TypedDict):
    name: str
    city_name: str

@dataclass
class ActivityData(TypedDict):
    id: str
    completed_streets: int
    date: str
    distance: float
    streets: List[Street]