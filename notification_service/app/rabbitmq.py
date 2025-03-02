import pika
import json
import os
from .db import get_db
from .models import Notification
from motor.motor_asyncio import AsyncIOMotorDatabase

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE", "recommendation_queue")

def consume_messages():
    """
    Listens for messages on the RabbitMQ queue and processes them.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Declare queue in case it's not already created
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    def callback(ch, method, properties, body):
        """
        Handles incoming messages.
        """
        message = json.loads(body)

        # Insert into MongoDB
        db = get_db()
        notification = Notification(
            user_id=message["user_id"],
            type=message["type"],
            content=message["content"]
        )
        db.notifications.insert_one(notification.dict())

        print(f" [x] Received Notification for User {message['user_id']}")

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    print(" [*] Waiting for messages. To exit, press CTRL+C")
    channel.start_consuming()
