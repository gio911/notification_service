import aio_pika
from config.config import (
    COMMON_CREATE_ROUTING_KEY,
    COMMON_MAIL_ROUTING_KEY,
    COMMON_REGISTER_ROUTING_KEY,
    COMMON_USER_ROUTING_KEY,
    NOTIFICATION_EXCHANGE,
    NOTIFICATION_QUEUE,
    MAIL_GENERATE_QUEUE,
    MAIL_SEND_QUEUE,
    USER_REGISTRATION_QUEUE,
    settings
)


async def setup_rabbitmq():
    connection = await aio_pika.connect_robust(
        f'amqp://{settings.rmq_user}:{settings.rmq_password}@{settings.rmq_host}:5672/'
    )
    async with connection:
        channel = await connection.channel()

        # Создаём Exchange (например, типа "topic")
        exchange = await channel.declare_exchange(
            NOTIFICATION_EXCHANGE, aio_pika.ExchangeType.TOPIC, durable=True
        )

        # Создаём очереди
        queue_new_film_notif = await channel.declare_queue(
            NOTIFICATION_QUEUE, durable=True
        )
        await queue_new_film_notif.bind(
            exchange, routing_key=COMMON_USER_ROUTING_KEY
        )

        queue_mail_generate = await channel.declare_queue(
            MAIL_GENERATE_QUEUE, durable=True
        )
        await queue_mail_generate.bind(
            exchange, routing_key=COMMON_MAIL_ROUTING_KEY
        )

        queue_email_send = await channel.declare_queue(
            MAIL_SEND_QUEUE, durable=True
        )
        await queue_email_send.bind(
            exchange, routing_key=COMMON_CREATE_ROUTING_KEY
        )

        queue_email_send = await channel.declare_queue(
            USER_REGISTRATION_QUEUE, durable=True
        )
        await queue_email_send.bind(
            exchange, routing_key=COMMON_REGISTER_ROUTING_KEY
        )

        print('RabbitMQ настроен!')
