from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.consumer import Consumer
from app import repository
from app.resolver import PropertyResolver
from typing import Optional
from app.populate_db import DataInit
from typing import List
from app.dbmodel import ActivityDict, StreetDict
from app.model import ActivityBase, StreetBase, ProgressBase, ProgressDict, MapProgressBase


origins = [
    "http://localhost",
    "http://localhost:4200"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

properties = PropertyResolver()

repo = repository.StreetRepository(properties.db_url)

dinit = DataInit()
if(dinit.test(properties.initial_data_file, repo)):
    dinit.populate(properties.initial_data_file, repo)

consumer = Consumer(repo)
consumer.connect(properties.rabbit, properties.rabbit_port)
consumer.start()

@app.get("/activities", response_model=List[ActivityBase])
async def activities(page: Optional[int] = None) -> List[ActivityDict]:
    result = repo.get_all_activities(page if page else 0)
    return [i.serialize for i in result]

@app.get("/streets", response_model=List[StreetBase])
async def streets(page: Optional[int] = None, area: Optional[str] = None) -> List[StreetDict]:
    result = repo.get_all_streets_for_area(area, page if page else 0) if area else repo.get_all_streets(page if page else 0)

    return [i.serialize for i in result]

@app.get("/streets/progress", response_model=ProgressBase)
async def progress(area: Optional[str] = None) -> ProgressDict:
    total = repo.get_total_streets(area if area else 'Wrocław')
    completed = repo.count_streets_by_area(area) if area else repo.count_streets_by_city('Wrocław')
    progress = completed/total if total > 0 else 0.
    return { 'total': total, 'completed': completed, 'progress':  "{0:.2%}".format(progress), 'city_completed': completed >= total }

@app.get("/map", response_model=List[MapProgressBase])
async def map_data() -> List[dict]:
    data = repo.get_map_data()
    result: List = []
    for d in data:
        name = d[0]
        total = d[1]
        completed = d[2]
        progress = completed/total if total > 0 else 0.
        result.append( { 'name': name, 'total': total, 'completed': completed, 'progress':  "{0:.2%}".format(progress), 'area_completed': completed >= total })
    return result


@app.on_event("shutdown")
async def shutdown_event() -> None:
    consumer.stop()
