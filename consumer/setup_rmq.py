import aio_pika

async def setup_rabbitmq():
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq:5672/")
    async with connection:
        channel = await connection.channel()

        # Создаём Exchange (например, типа "topic")
        exchange = await channel.declare_exchange("notification_exchange", aio_pika.ExchangeType.TOPIC, durable=True)

        # Создаём очереди
        queue_new_film_notif = await channel.declare_queue("new_film_notif_queue", durable=True)
        await queue_new_film_notif.bind(exchange, routing_key="user.*")  

        queue_mail_generate = await channel.declare_queue("mail_generate", durable=True)
        await queue_mail_generate.bind(exchange, routing_key="mail.*")  

        queue_email_send = await channel.declare_queue("email_send", durable=True)
        await queue_email_send.bind(exchange, routing_key="create.*")  
        
        queue_email_send = await channel.declare_queue("users_registration", durable=True)
        await queue_email_send.bind(exchange, routing_key="register.*")  

        print("RabbitMQ настроен!")
