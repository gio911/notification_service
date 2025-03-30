import aio_pika

async def setup_rabbitmq():
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq:5672/")
    async with connection:
        channel = await connection.channel()

        # Создаём Exchange (например, типа "topic")
        exchange = await channel.declare_exchange("notification_exchange", aio_pika.ExchangeType.TOPIC, durable=True)

        # Создаём очереди
        queue_new_film_notif = await channel.declare_queue("new_film_notif_queue", durable=True)
        await queue_new_film_notif.bind(exchange, routing_key="user.*")  # Получает email-уведомления

        queue_mail_generate = await channel.declare_queue("mail_generate", durable=True)
        await queue_mail_generate.bind(exchange, routing_key="mail.*")  # Получает лайки

        queue_general = await channel.declare_queue("general_queue", durable=True)
        await queue_general.bind(exchange, routing_key="general.event")  # Для других событий

        print("RabbitMQ настроен!")
