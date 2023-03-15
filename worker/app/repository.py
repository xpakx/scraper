import hashlib
import logging
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
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

engine = create_engine('sqlite:///pages.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def calculate_hash(page: str) -> str:
    return hashlib.sha256(str(page).encode("utf-8")).hexdigest()

def load_hash(url: str) -> Optional[str]:
    session = Session()
    page = session.query(Page).filter(Page.url == url).first()
    if page:
        return str(page.hash)
    return None

def update_hash(url: str, hash_value: str) -> None:
    session = Session()
    page = session.query(Page).filter(Page.url == url).first()
    if page:
        page.hash = hash_value
    else:
        session.add(Page(url=url, hash=hash_value))
    session.commit()

def test_changes(url: str, title: str) -> bool:
    hash: str = calculate_hash(title)
    oldHash: Optional[str] = load_hash(url)
    if(oldHash == None or oldHash != hash):
        update_hash(url, hash)
        logger.info("Page changed")
        return True
    else:
        logger.info("Page not changed")
        return False