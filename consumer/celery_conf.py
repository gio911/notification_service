
from celery import Celery
from kombu import Queue, Exchange

celery_app = Celery(
    'consumer',
    broker='pyamqp://guest:guest@rabbitmq:5672//',
    include=["tasks.email"]
)

celery_app.conf.task_queues = [
    Queue("email_queue", Exchange("notification_exchange", type="topic", durable=True), routing_key="email.send")
]

celery_app.conf.task_routes = {"tasks.email.send_email": {"queue": "email_queue"}}