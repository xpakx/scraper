from fastapi import FastAPI
from consumer import Consumer
import repository

app = FastAPI()
consumer = Consumer()
consumer.connect('localhost', 5672)
consumer.start()

@app.get("/activities")
async def activities():
    return repository.get_all_activities()

@app.on_event("shutdown")
async def shutdown_event():
    consumer.stop()