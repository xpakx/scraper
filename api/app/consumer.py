import pika
import threading
from app.repository import StreetRepository
from app.data import ActivityData
import json

class Consumer:
    def __init__(self, repo: StreetRepository):
        self.repo = repo

    def connect(self, host: str, port: int) -> None:
        params = pika.ConnectionParameters(host = host, port = port)
        self.connection = pika.BlockingConnection(parameters=params)
        self.channel = self.connection.channel()

    def consume_messages(self) -> None:
        self.channel.queue_declare(queue='pages.queue')
        self.channel.basic_consume(queue='pages.queue', on_message_callback=self.process_message, auto_ack=True)
        self.channel.start_consuming()

    def process_message(self, channel, method, properties, body) -> None: #type: ignore
        print(f"Received message: {body.decode()}")
        self.repo.add_activity(ActivityData(**json.loads(body.decode())))

    def start(self) -> None:
        self.thread = threading.Thread(target=self.consume_messages)
        self.thread.start()

    def stop(self) -> None:
        self.channel.stop_consuming()
        self.thread.join()
        self.connection.close()