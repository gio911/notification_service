from settings import RabbitMQConsumer
import asyncio

async def main():
    consumer = RabbitMQConsumer()
    await consumer.connect()
    await consumer.consume()
    
if __name__=="__main__":
    asyncio.run(main())
    