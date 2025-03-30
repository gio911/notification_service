import asyncio
import aio_pika
import json 
# from aio_pika import connect_robust
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from setup_rmq import setup_rabbitmq
from celery_app import transfer_to_auth_service, transfer_to_deliver_service
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

            if self.queue_name == 'new_film_notif_queue':
                # Получаем очередь
                queue = await channel.get_queue(self.queue_name, ensure=True)
                # Подписываемся на очередь и начинаем обрабатывать сообщения
                await queue.consume(self.process_request_user_data)
                print(f"Consumer started, listening on {self.queue_name}...")

                await asyncio.Future()  # Чтобы не завершалась программа
            
            elif self.queue_name == 'mail_generate':
                # Получаем очередь
                queue = await channel.get_queue(self.queue_name, ensure=True)
                # Подписываемся на очередь и начинаем обрабатывать сообщения
                await queue.consume(self.process_email_transfer)
                print(f"Consumer started, listening on {self.queue_name}...")

                await asyncio.Future()  # Чтобы не завершалась программа
             
             
             
             
                
    async def process_email_transfer(self, message: aio_pika.IncomingMessage):
        print(message,90900) 
        async with message.process():
            print(182)
            body = json.loads(message.body.decode())    
            print(f"Received email message: {body}")

            # Извлекаем данные
            first_name=body['first_name']
            email=body['email']  
            
            print(first_name, email, 9009)
            transfer_to_deliver_service.delay(first_name, email)      
                
    async def process_request_user_data(self, message: aio_pika.IncomingMessage):
        async with message.process():
            print(172)
            body = json.loads(message.body.decode())    
            print(f"Received email message: {body}")

            # Извлекаем данные
            user_id=body['user_id']
            token=body['token']

            # Отправка письма через Celery
            transfer_to_auth_service.delay(user_id, token)
            print("Email send task has been queued")


async def main():
   # Запускаем настройку RabbitMQ
    await setup_rabbitmq()

    # Создаём и подключаем consumers
    consumer1 = Consumer('new_film_notif_queue')
    consumer2 = Consumer('mail_generate')
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