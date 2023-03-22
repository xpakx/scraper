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