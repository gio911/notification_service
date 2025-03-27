import time
import socket


def wait_for_rabbitmq(host, port):
    while True:
        try:
            with socket.create_connection((host, port), timeout=3):
                print("RabbitMQ доступен")
                break
        except OSError:
            print("Ожидание RsbbitMQ...")
            time.sleep(2)
