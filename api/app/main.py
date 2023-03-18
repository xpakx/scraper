from fastapi import FastAPI
from consumer import Consumer

app = FastAPI()
consumer = Consumer()
consumer.connect('localhost', 5672)
consumer.start()


@app.get("/activities")
async def activities():
    return {"text": "Test"}

@app.on_event("shutdown")
async def shutdown_event():
    consumer.stop()