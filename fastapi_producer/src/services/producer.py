from functools import lru_cache
import aio_pika
import json
import logging

from fastapi import Depends
from src.db.rmq import get_rabbitmq_connection
from src.core.logging_config import setup_logging


logger = setup_logging()


class Producer:
    def __init__(self, rabbitmq_conn):
        self.rabbitmq_conn = rabbitmq_conn

    async def send_to_queue(
        self,
        message: dict,
        routing_key,
    ) -> None:
        try:
            async with self.rabbitmq_conn.channel() as channel:
                exchange = await channel.declare_exchange(
                    'notification_exchange',
                    aio_pika.ExchangeType.TOPIC,
                    durable=True,
                )

                await exchange.publish(
                    aio_pika.Message(
                        body=json.dumps(message).encode(),
                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    ),
                    routing_key=routing_key,  # Ключ маршрутизации
                )

                logger.info(
                    'Сообщение успешно отправлено в очередь с routing_key=%s',
                    routing_key,
                )
        except Exception as e:
            logger.error('Ошибка при отправке сообщения в очередь: %s', str(e))
            raise


@lru_cache
def get_rmq_publisher_service(
    rabbitmq_connection=Depends(get_rabbitmq_connection),
) -> Producer:
    return Producer(rabbitmq_connection)
