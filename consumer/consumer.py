import asyncio
import aio_pika
import json 
# from aio_pika import connect_robust
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from setup_rmq import setup_rabbitmq
from celery_app import send_email
import subprocess


class Consumer:
    def __init__(self, queue_name, connection_url="amqp://guest:guest@rabbitmq:5672/"):
        self.connection_url = connection_url
        self.rabbitmq_conn = None
        self.queue_name=queue_name
        
    async def connect(self):
        self.rabbitmq_conn = await aio_pika.connect_robust(self.connection_url)
        
    async def close(self):
        if self.rabbitmq_conn and not self.rabbitmq_conn.is_closed:
            self.rabbitmq_conn.close()
              
    async def process_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body = json.loads(message.body.decode())
            print(f"Received: {body}")
     
    async def consume(self):
        # Подключаемся к RabbitMQ и получаем канал
        async with self.rabbitmq_conn:
            channel = await self.rabbitmq_conn.channel()

            # Получаем очередь
            queue = await channel.get_queue(self.queue_name, ensure=True)

            # Подписываемся на очередь и начинаем обрабатывать сообщения
            await queue.consume(self.process_send_email)
            print(f"Consumer started, listening on {self.queue_name}...")

            await asyncio.Future()  # Чтобы не завершалась программа
            
 
    async def process_send_email(self, message: aio_pika.IncomingMessage):
        async with message.process():
            print(172)
            body = json.loads(message.body.decode())    
            print(f"Received email message: {body}")

            # Извлекаем данные
            recipient = body['recipient']
            subject = body['subject']
            body_text = body['body']

            # Отправка письма через Celery
            send_email.delay(recipient, subject, body_text)
            print("Email send task has been queued")


async def main():
   # Запускаем настройку RabbitMQ
    await setup_rabbitmq()

    # Создаём и подключаем consumers
    consumer1 = Consumer('email_queue')
    consumer2 = Consumer('likes_queue')
    await consumer1.connect()
    await consumer2.connect()

    # Запускаем Celery Worker в отдельном процессе
    celery_process = subprocess.Popen(['celery', '-A', 'celery_app', 'worker', '--loglevel=info'])

    # Потребляем сообщения
    await asyncio.gather(consumer1.consume(), consumer2.consume())

    # Закрываем процесс Celery при завершении
    celery_process.terminate()
    celery_process.wait()
    
if __name__=="__main__":
    asyncio.run(main())
    
    
    
# qwerty123321!

# cbtj vhsa lfpn opfu