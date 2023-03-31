from pydantic import BaseModel
from typing import TypedDict

class ActivityBase(BaseModel):
    id: int
    activity_id: str
    completed_streets: int
    date: str
    distance: float

class StreetBase(BaseModel):
    id: int
    name: str
    city_name: str
    activity_id: str
    date: str
    areas: str

class ProgressDict(TypedDict):
    total: int
    completed: int
    progress:  str
    city_completed: bool

class ProgressBase(BaseModel):
    total: int
    completed: int
    progress:  str
    city_completed: bool