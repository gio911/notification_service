import asyncio
import aio_pika
import json 
# from aio_pika import connect_robust

class RabbitMQConsumer:
    def __init__(self, connection_url="amqp://guest:guest@rabbitmq:5672/"):
        self.connection_url = connection_url
        self.rabbitmq_conn = None
        
    async def connect(self):
        self.rabbitmq_conn = await aio_pika.connect_robust(self.connection_url)
        
    async def close(self):
        if self.rabbitmq_conn and not self.rabbitmq_conn.is_closed:
            self.rabbitmq_conn.close()
              
    async def process_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body = json.loads(message.body.decode())
            print(f"Received: {body}")
     
    async def consume(self, queue_name:str = "email_queue", exchange_name: str = "notification_exchange"):
        channel = await self.rabbitmq_conn.channel()
        exchange = await channel.declare_exchange(exchange_name, "topic", durable=True)
        queue = await channel.declare_queue(queue_name, durable=True)
        await queue.bind(exchange=exchange, routing_key="email.*")
        await queue.consume(self.process_message)
        print("Consumer started...")
        await asyncio.Future() 
            
 
            
