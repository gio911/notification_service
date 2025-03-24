import asyncio
import aio_pika
import json 
# from aio_pika import connect_robust
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
        await queue.consume(self.process_send_email)
        print("Consumer started...")
        await asyncio.Future() 
            
 
    async def process_send_email(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body = json.loads(message.body.decode())
            print(f"Received email message: {body}")

            # Извлекаем данные
            recipient = body['recipient']
            subject = body['subject']
            body_text = body['body']

            # Создаем email
            msg = MIMEMultipart()
            msg['From'] = "rmqapp@gmail.com"
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body_text, 'plain'))

            # Отправка письма через SMTP
            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login("rmqapp@gmail.com", "cbtjvhsalfpnopfu")
                    server.sendmail("rmqapp@gmail.com", recipient, msg.as_string())
                    print("Email sent successfully")
            except Exception as e:
                print(f"Error sending email: {e}")       


# qwerty123321!

# cbtj vhsa lfpn opfu