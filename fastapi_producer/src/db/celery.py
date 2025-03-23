from celery import Celery

celery: Celery | None = None


# Функция понадобится при внедрении зависимостей
async def get_celery() -> Celery:
    return celery
