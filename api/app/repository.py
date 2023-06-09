import logging
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from app.data import ActivityData
from app.data import Street as ActivityDataStreet
from typing import List
from app.dbmodel import Activity, Street, StreetData, AreaData
from app.db import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StreetRepository():
    def __init__(self, url: str):
        self.engine = create_engine(url)
        self.Base = Base
        Base.metadata.create_all(self.engine) #type: ignore
        self.Session = sessionmaker(bind=self.engine)

    def add_activity(self, data: ActivityData) -> None:
        session = self.Session()
        session.add(Activity(
            activity_id=data['id'], 
            completed_streets=data['completed_streets'],
            date=data['date'],
            distance=data['distance']
        ))
        logger.info(data['streets'])
        for street in data['streets']:
            self.add_street(data, session, street)
        session.commit()

    def add_street(self, data: ActivityData, session, street: ActivityDataStreet) -> None: #type: ignore
        logger.info(street)
        areas = session.query(StreetData.areas).filter(StreetData.name == street['name']).first()
        session.add(Street(
                name=street['name'], 
                city_name=street['city_name'],
                activity_id=data['id'],
                date=data['date'],
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
    
    def get_map_data(self) -> List:
        session = self.Session()
        return session.query(AreaData.name, AreaData.streets, func.count(Street.id)).\
            select_from(AreaData).\
            join(Street, Street.areas.like('%' + AreaData.name + '%')).\
            group_by(AreaData.id).\
            having(AreaData.name.not_like("Wrocław")).\
            all()