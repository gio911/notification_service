from functools import lru_cache
# from aio_pika import connect_robust
import aio_pika
import json

from fastapi import Depends
from src.db.rmq import get_rabbitmq_connection


class Producer:
    def __init__(self, rabbitmq_conn:aio_pika.RobustConnection):
        self.rabbitmq_conn=rabbitmq_conn

    
    async def send_to_queue(
        self,
        message: dict,
        routing_key: str
    ) -> None:
        async with self.rabbitmq_conn.channel() as channel:
            # Объявляем exchange
            exchange = await channel.declare_exchange(
                "notification_exchange", 
                aio_pika.ExchangeType.TOPIC, 
                durable=True
            )

            # Создаем очередь
            queue = await channel.declare_queue("email_queue", durable=True)

            # Привязываем очередь к exchange с заданным routing_key
            await queue.bind(exchange, routing_key=routing_key)
    
            # Публикуем сообщение в exchange с routing_key
            await exchange.publish(
                aio_pika.Message(
                    body=json.dumps(message).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=routing_key  # Ключ маршрутизации
            )
                
@lru_cache
def get_rmq_publisher_service(
    rabbitmq_connection=Depends(get_rabbitmq_connection),
)->Producer:
    return Producer(rabbitmq_connection)


