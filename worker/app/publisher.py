import pika
from data import ActivityData
import json
from dataclasses import asdict
from typing import List

class Publisher:
    connection = None
    channel = None

    def connect(self, host: str, port: int) -> None:
        params = pika.ConnectionParameters(host = host, port = port)
        self.connection = pika.BlockingConnection(parameters=params)
        self.channel = self.connection.channel()
    
    def setup(self) -> None:
        self.channel.exchange_declare('pages', exchange_type='direct')
        self.channel.queue_declare('pages.queue')
        self.channel.queue_bind(
            'pages.queue', 
            exchange='pages', 
            routing_key='page.changes'
        )

    def publish(self, payload: ActivityData) -> None:
        if(self.connection.is_open and self.channel.is_open):
            self.channel.basic_publish(
                exchange='pages', 
                routing_key='page.changes', 
                body = json.dumps(asdict(payload))
            )
        
    def publish_all(self, activities: List[ActivityData]) -> None:
        for activity in activities:
            self.publish(activity)
