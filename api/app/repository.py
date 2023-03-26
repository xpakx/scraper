import logging
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.data import ActivityData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class Activity(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    activity_id = Column(String)
    completed_streets = Column(Integer)
    date = Column(String)
    distance = Column(String)

class Street(Base):
    __tablename__ = 'streets'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city_name = Column(String)
    activity_id = Column(Integer)
    date = Column(String)

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

class StreetRepository():
    def __init__(self, url: str):
        self.engine = create_engine(url)
        self.Base = Base
        Base.metadata.create_all(self.engine)
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
            logger.info(street)
            session.add(Street(
                name=street['name'], 
                city_name=street['city_name'],
                activity_id=data.id,
                date=data.date
            ))
        session.commit()

    def get_all_activities(self, page: int = 0):
        session = self.Session()
        offset = page * 20
        return session.query(Activity).offset(offset).limit(20).all()

    def get_all_streets(self, page: int = 0):
        session = self.Session()
        offset = page * 20
        return session.query(Street).offset(offset).limit(20).all()
    
    def count_streets_by_city(self, city_name: str) -> int:
        session = self.Session()
        return session.query(Street).filter(Street.city_name == city_name).count()

    def add_area_data(self, data) -> None:
        session = self.Session()
        for area in data:
            session.add(AreaData(
            name=area['area'], 
            streets=int(area['street_count']),
        ))
        session.commit()

    def add_street_data(self, data) -> None:
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