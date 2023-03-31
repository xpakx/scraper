import logging
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.data import ActivityData
from app.data import Street as ActivityDataStreet
from typing import List, TypedDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class ActivityDict(TypedDict):
    id: int
    activity_id: str
    completed_streets: int
    date: str
    distance: float

class Activity(Base): #type: ignore
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

class Street(Base): #type: ignore
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

class StreetData(Base): #type: ignore
    __tablename__ = 'street_data'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    areas = Column(String)

class AreaData(Base): #type: ignore
    __tablename__ = 'area_data'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    streets = Column(Integer)

class StreetRepository():
    def __init__(self, url: str):
        self.engine = create_engine(url)
        self.Base = Base
        Base.metadata.create_all(self.engine) #type: ignore
        self.Session = sessionmaker(bind=self.engine)

    def add_activity(self, data: ActivityData) -> None:
        session = self.Session()
        session.add(Activity(
            activity_id=data.id, 
            completed_streets=data.completed_streets,
            date=data.date,
            distance=data.distance
        ))
        logger.info(data.streets)
        for street in data.streets:
            self.add_street(data, session, street)
        session.commit()

    def add_street(self, data: ActivityData, session, street) -> None:
        logger.info(street)
        areas = session.query(StreetData.areas).filter(StreetData.name == street['name']).first()
        session.add(Street(
                name=street['name'], 
                city_name=street['city_name'],
                activity_id=data.id,
                date=data.date,
                areas= str(areas) if areas else ''
            ))

    def get_all_activities(self, page: int = 0) -> List[Activity]:
        session = self.Session()
        offset = page * 20
        return session.query(Activity).offset(offset).limit(20).all()

    def get_all_streets(self, page: int = 0) -> List[Street]:
        session = self.Session()
        offset = page * 20
        return session.query(Street).offset(offset).limit(20).all()
    
    def count_streets_by_city(self, city_name: str) -> int:
        session = self.Session()
        return session.query(Street).filter(Street.city_name == city_name).count()

    def add_area_data(self, data: dict) -> None:
        session = self.Session()
        for area in data:
            session.add(AreaData(
            name=area['area'], 
            streets=int(area['street_count']),
        ))
        session.commit()

    def add_street_data(self, data: dict) -> None:
        session = self.Session()
        for street in data:
            session.add(StreetData(
            name=street['name'], 
            areas=';' + ';'.join(street['areas']) + ';',
        ))
        session.commit()

    def has_areas_data(self) -> bool:
        session = self.Session()
        return session.query(AreaData).first() is not None
    
    def get_all_streets_for_area(self, area: str, page: int = 0) -> List[Street]:
        session = self.Session()
        offset = page * 20
        return session.query(Street).filter(Street.areas.like(f'%;{area};%')).offset(offset).limit(20).all()
    
    def get_total_streets(self, area: str) -> int:
        session = self.Session()
        streets = session.query(AreaData.streets).filter(AreaData.name == area).first()
        return int(streets[0]) if streets else 0
    
    def count_streets_by_area(self, area: str) -> int:
        session = self.Session()
        return session.query(Street).filter(Street.areas.like(f'%;{area};%')).count()