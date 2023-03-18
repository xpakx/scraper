import logging
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from data import ActivityData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class Activity(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    activity_id = Column(String)
    completed_streets = Column(Integer)
    date = Column(String)
    distance = Column(String)

engine = create_engine('sqlite:///pages.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def add_activity(data: ActivityData) -> None:
    print(f"Received message: {data}")
    session = Session()
    session.add(Activity(
        activity_id=data.id, 
        completed_streets=data.completed_streets,
        date=data.date,
        distance=data.distance
    ))
    session.commit()
