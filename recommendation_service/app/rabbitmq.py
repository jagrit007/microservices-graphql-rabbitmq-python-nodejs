import pika
import json
import os

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "user")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "password")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE", "recommendation_queue")

def publish_message(message: dict):
    """
    Publishes a message to the RabbitMQ queue with authentication.
    """
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    )
    channel = connection.channel()

    # Declare the queue (in case it's not already created)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Publish the message
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2  # Makes the message persistent
        ),
    )

    connection.close()
