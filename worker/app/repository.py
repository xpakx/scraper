import hashlib
import logging
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    hash = Column(String)
    def __repr__(self) -> str:
        return f"<Page(url='{self.url}', hash='{self.hash}')>"

class PageRepository:
    def __init__(self, url: str):
        self.engine = create_engine(url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def calculate_hash(self, page: str) -> str:
        return hashlib.sha256(str(page).encode("utf-8")).hexdigest()

    def load_hash(self, url: str) -> Optional[str]:
        session = self.Session()
        page = session.query(Page).filter(Page.url == url).first()
        if page:
            return str(page.hash)
        return None

    def update_hash(self, url: str, hash_value: str) -> None:
        session = self.Session()
        page = session.query(Page).filter(Page.url == url).first()
        if page:
            page.hash = hash_value
        else:
            session.add(Page(url=url, hash=hash_value))
        session.commit()

    def test_changes(self, url: str, title: str) -> bool:
        hash: str = self.calculate_hash(title)
        oldHash: Optional[str] = self.load_hash(url)
        if(oldHash == None or oldHash != hash):
            self.update_hash(url, hash)
            logger.info("Page changed")
            return True
        else:
            logger.info("Page not changed")
            return False