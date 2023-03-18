from dataclasses import dataclass

@dataclass
class ActivityData:
    id: str
    completed_streets: int
    date: str
    distance: str