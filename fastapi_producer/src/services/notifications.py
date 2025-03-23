from functools import lru_cache
# from aio_pika import connect_robust
import aio_pika
import json

from fastapi import Depends
from src.db.rmq import get_rabbitmq_connection


class RabbitMQPublisherService:
    def __init__(self, rabbitmq_conn):
        self.rabbitmq_conn=rabbitmq_conn


    async def send_to_queue(
        self,
        message: dict,
        routing_key: str = "email.send",
        queue_name: str = "email_queue",
        exchange_name: str = "notification_exchange",
        binding_key: str = "email.*"
        )->None:
            channel = await self.rabbitmq_conn.channel()
            exchange = await channel.declare_exchange(exchange_name, "topic", durable=True)
            queue = await channel.declare_queue(queue_name, durable=True)
            await queue.bind(exchange=exchange, routing_key=binding_key)
            await exchange.publish(
                aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=routing_key
        )
                
@lru_cache
def get_rmq_publisher_service(
    rabbitmq_connection=Depends(get_rabbitmq_connection),
)->RabbitMQPublisherService:
    return RabbitMQPublisherService(rabbitmq_connection)


