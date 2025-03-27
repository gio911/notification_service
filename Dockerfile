FROM python:3.9-slim

# Устанавливаем зависимости для Flower
RUN pip install flower

# Открываем нужный порт
EXPOSE 5555

# Запускаем Flower
CMD ["flower", "--port=5555", "--broker=pyamqp://guest:guest@rabbitmq//"]
