from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from consumer import Consumer
import repository

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

consumer = Consumer()
consumer.connect('localhost', 5672)
consumer.start()

@app.get("/activities")
async def activities():
    return repository.get_all_activities()

@app.on_event("shutdown")
async def shutdown_event():
    consumer.stop()