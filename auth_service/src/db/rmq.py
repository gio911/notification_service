import aio_pika

rabbitmq_connection = None

def get_rabbitmq_connection():
    return rabbitmq_connection