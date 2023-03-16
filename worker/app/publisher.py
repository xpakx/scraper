import pika
from data import PageData

class Publisher:
    connection = None
    channel = None

    def connect(self):
        params = pika.ConnectionParameters(host = 'localhost', port = 5672)
        self.connection = pika.BlockingConnection(parameters=params)
        self.channel = self.connection.channel()
    
    def setup(self):
        self.channel.exchange_declare('pages', exchange_type='direct')
        self.channel.queue_declare('Page changes')
        self.channel.queue_bind('Page changes', exchange='pages', routing_key='page.changes')

    def publish(self, payload: PageData):
        if(self.connection.is_open and self.channel.is_open):
            self.channel.basic_publish(exchange='pages', routing_key='page.changes', body = payload)
        