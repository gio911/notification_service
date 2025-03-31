import asyncio
import aio_pika
import json 
from setup_rmq import setup_rabbitmq
from celery_app import transfer_to_auth_service, transfer_to_deliver_service, send_email
import subprocess
from config.logging_config import setup_logging

logger = setup_logging()


BATCH_SIZE = 10  # Количество писем в батче
BATCH_TIMEOUT = 30  # Таймаут для отправки (секунд)

class Consumer:
    def __init__(self, queue_name, connection_url="amqp://guest:guest@rabbitmq:5672/"):
        self.connection_url = connection_url
        self.rabbitmq_conn = None
        self.queue_name = queue_name
        self.batch = []
        self.batch_timer = None
        
    async def connect(self):
        self.rabbitmq_conn = await aio_pika.connect_robust(self.connection_url)
        logger.info(f"Подключение к RabbitMQ на {self.connection_url} успешно")

    async def close(self):
        if self.rabbitmq_conn and not self.rabbitmq_conn.is_closed:
            self.rabbitmq_conn.close()
            logger.info("Соединение с RabbitMQ закрыто")
              
    async def process_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body = json.loads(message.body.decode())
            logger.info(f"Получено сообщение: {body}")
     
    async def consume(self):
        # Подключаемся к RabbitMQ и получаем канал
        async with self.rabbitmq_conn:
            channel = await self.rabbitmq_conn.channel()

            if self.queue_name == 'new_film_notif_queue':
                # Получаем очередь
                queue = await channel.get_queue(self.queue_name, ensure=True)
                # Подписываемся на очередь и начинаем обрабатывать сообщения
                await queue.consume(self.process_request_user_data)
                logger.info(f"Потребитель запущен, прослушиваем очередь {self.queue_name}...")

                await asyncio.Future()  # Чтобы не завершалась программа
            
            elif self.queue_name == 'mail_generate':
                # Получаем очередь
                queue = await channel.get_queue(self.queue_name, ensure=True)
                # Подписываемся на очередь и начинаем обрабатывать сообщения
                await queue.consume(self.process_email_transfer)
                logger.info(f"Потребитель запущен, прослушиваем очередь {self.queue_name}...")

                await asyncio.Future()  # Чтобы не завершалась программа
            
            elif self.queue_name == "email_send":
                logger.info("Запуск потребителя для отправки пачки писем")

                # Получаем очередь
                queue = await channel.get_queue(self.queue_name, ensure=True)
                # Подписываемся на очередь и начинаем обрабатывать сообщения
                await queue.consume(self.process_send_email)
                logger.info(f"Потребитель запущен, прослушиваем очередь {self.queue_name}...")
                self.batch_timer = asyncio.create_task(self.batch_timeout())
                await asyncio.Future()  # Чтобы не завершалась программа
    
    async def batch_timeout(self):
        """Ждет BATCH_TIMEOUT секунд и отправляет письма, если они есть"""
        while True:
            await asyncio.sleep(BATCH_TIMEOUT)
            if self.batch:
                logger.info(f"Время ожидания пачки писем истекло, отправляем {len(self.batch)} писем.")
                await self.send_batch()
                
    async def send_batch(self):
        """Отправляет письма пачкой"""
        for email_data in self.batch:
            send_email.delay(email_data["email"], email_data["first_name"])
        self.batch.clear()  # Очищаем батч после отправки
        logger.info(f"Отправлено {len(self.batch)} писем.")

    async def process_send_email(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body = json.loads(message.body.decode())    
            logger.info(f"Получено сообщение для отправки письма: {body}")
            self.batch.append(body)
            if len(self.batch) >= BATCH_SIZE:
                await self.send_batch()
                
    async def process_email_transfer(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body = json.loads(message.body.decode())    
            logger.info(f"Получено сообщение для передачи данных по email: {body}")

            first_name = body['first_name']
            email = body['email']  
            
            logger.info(f"Обрабатываем передачу данных для {first_name} ({email})")
            transfer_to_deliver_service.delay(first_name, email)      


    async def process_request_user_data(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body = json.loads(message.body.decode())    
            logger.info(f"Получено сообщение с данными пользователя: {body}")

            user_id = body['user_id']
            token = body['token']

            logger.info(f"Обрабатываем данные для пользователя с ID: {user_id}")
            transfer_to_auth_service.delay(user_id, token)
            logger.info("Задача на отправку письма поставлена в очередь")
            
    
    async def process_user_registration(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body = json.loads(message.body.decode())    
            logger.info(f"Получено сообщение с данными пользователя: {body}")

            user_name = body['name']
            user_email = body['email']

            logger.info(f"Обрабатываем данные для пользователя с ID: {user_name}")
            transfer_to_auth_service.delay(user_name, user_email)
            logger.info("Задача на отправку письма поставлена в очередь")
            
            
async def main():
   # Запускаем настройку RabbitMQ
    await setup_rabbitmq()

    # Создаём и подключаем consumers
    consumer1 = Consumer('new_film_notif_queue')
    consumer2 = Consumer('mail_generate')
    consumer3 = Consumer('email_send')
    
    await consumer1.connect()
    await consumer2.connect()
    await consumer3.connect()

    # Запускаем Celery Worker в отдельном процессе
    celery_process = subprocess.Popen(['celery', '-A', 'celery_app', 'worker', '--loglevel=info'])

    # Потребляем сообщения
    await asyncio.gather(consumer1.consume(), consumer2.consume(), consumer3.consume())

    # Закрываем процесс Celery при завершении
    celery_process.terminate()
    celery_process.wait()

if __name__ == "__main__":
    asyncio.run(main())