import pika
import threading

class Consumer:
    def connect(self, host: str, port: int) -> None:
        params = pika.ConnectionParameters(host = host, port = port)
        self.connection = pika.BlockingConnection(parameters=params)
        self.channel = self.connection.channel()

    def consume_messages(self):
        self.channel.queue_declare(queue='pages.queue')
        self.channel.basic_consume(queue='pages.queue', on_message_callback=self.process_message, auto_ack=True)
        self.channel.start_consuming()

    def process_message(self, channel, method, properties, body):
        print(f"Received message: {body.decode()}")

    def start(self):
        self.thread = threading.Thread(target=self.consume_messages)
        self.thread.start()

    def stop(self):
        self.channel.stop_consuming()
        self.thread.join()
        self.connection.close()