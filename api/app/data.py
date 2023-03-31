from typing import List, TypedDict

class Street(TypedDict):
    name: str
    city_name: str

class ActivityData(TypedDict):
    id: str
    completed_streets: int
    date: str
    distance: float
    streets: List[Street]