import aio_pika

rabbitmq_connection:aio_pika.RobustConnection = None

def get_rabbitmq_connection():
    return rabbitmq_connection