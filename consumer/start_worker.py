from waiter_rmq import wait_for_rabbitmq
import subprocess


wait_for_rabbitmq("rabbitmq", 5672)

print("Запуск Celery Worker...")
subprocess.run(["celery", "-A", "celery_conf", "worker", "--loglevel=info"])



# celery -A celery_conf worker --loglevel=info