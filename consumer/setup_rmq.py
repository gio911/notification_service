# import aio_pika

# async def setup_rabbitmq():
#     connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq:5672/")
#     async with connection:
#         channel = await connection.channel()

#         # Создаём Exchange (например, типа "topic")
#         exchange = await channel.declare_exchange("notification_exchange", aio_pika.ExchangeType.TOPIC, durable=True)

#         # Создаём очереди
#         queue_email = await channel.declare_queue("email_queue", durable=True)
#         await queue_email.bind(exchange, routing_key="email.*")  # Получает email-уведомления

#         queue_likes = await channel.declare_queue("likes_queue", durable=True)
#         await queue_likes.bind(exchange, routing_key="like.*")  # Получает лайки

#         queue_general = await channel.declare_queue("general_queue", durable=True)
#         await queue_general.bind(exchange, routing_key="general.event")  # Для других событий

#         print("RabbitMQ настроен!")

