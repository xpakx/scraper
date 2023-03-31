from app.db import Base
from typing import TypedDict
from sqlalchemy import Column, Integer, String, Float


class ActivityDict(TypedDict):
    id: int
    activity_id: str
    completed_streets: int
    date: str
    distance: float

class Activity(Base): 
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    activity_id = Column(String)
    completed_streets = Column(Integer)
    date = Column(String)
    distance = Column(Float)

    @property
    def serialize(self) -> ActivityDict:
        return {
            'id': int(self.id), 
            'activity_id': str(self.activity_id),
            'completed_streets': int(self.completed_streets),
            'date': str(self.date),
            'distance': float(self.distance)
        }

class StreetDict(TypedDict):
    id: int
    name: str
    city_name: str
    activity_id: int
    date: str
    areas: str

class Street(Base): 
    __tablename__ = 'streets'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city_name = Column(String)
    activity_id = Column(Integer)
    date = Column(String)
    areas = Column(String)

    @property
    def serialize(self) -> StreetDict:
        return {
            'id': int(self.id), 
            'name': str(self.name),
            'city_name': str(self.city_name),
            'activity_id': int(self.activity_id),
            'date': str(self.date),
            'areas': str(self.areas)
        }

class StreetData(Base): 
    __tablename__ = 'street_data'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    areas = Column(String)

class AreaData(Base): 
    __tablename__ = 'area_data'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    streets = Column(Integer)