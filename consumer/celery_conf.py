
from celery import Celery
from kombu import Queue, Exchange
from celery.signals import task_prerun

celery_app = Celery(
    'consumer',
    broker='pyamqp://guest:guest@rabbitmq:5672//',
    include=["tasks.email"]
)

@task_prerun.connect
def before_task_run(task, **kwargs):
    # task.args и task.kwargs содержат параметры, переданные в задачу
    # Здесь вы можете изменить аргументы задачи или логировать их
    print(f"Message received by task {task.name} with args: {task.args} and kwargs: {task.kwargs}")


# Определяем exchange и очередь, откуда Celery будет слушать задачи
# notification_exchange = Exchange("notification_exchange", type="topic", durable=True)

celery_app.conf.task_queues = [
    Queue("email_queue", Exchange("notification_exchange", type="topic", durable=True), routing_key="email.send")
]

celery_app.conf.task_routes = {"tasks.email.send_email": {"queue": "email_queue"}}