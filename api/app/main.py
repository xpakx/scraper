from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.consumer import Consumer
from app import repository
from app.resolver import PropertyResolver
from typing import Optional

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

consumer = Consumer()
consumer.connect(properties.rabbit, properties.rabbit_port)
consumer.start()

@app.get("/activities")
async def activities(page: Optional[int] = None):
    return repository.get_all_activities(page if page else 0)

@app.get("/streets")
async def streets(page: Optional[int] = None):
    return repository.get_all_streets(page if page else 0)

@app.on_event("shutdown")
async def shutdown_event():
    consumer.stop()
