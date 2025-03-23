from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from src.core.config import settings
from src.db import rmq
from src.db.database import AsyncSessionLocal
from celery import Celery
from src.api.endpoints import notifications
import aio_pika


# Создаем экземпляр FastAPI
@asynccontextmanager
async def lifespan(_: FastAPI):
    # redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)
    # session.session = AsyncSessionLocal()
    # celery.celery = Celery("notification_service", broker=settings.redis_broker_url, backend=settings.redis_backend_url)
    rmq.rabbitmq_connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq:5672/")
    
    yield

    # Закрытие соединений при завершении работы
    # await redis.redis.close()
    # await session.session.close()
    # await celery.celery.close()
    await rmq.rabbitmq_connection.close()

# Один экземпляр FastAPI
app = FastAPI(
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

# # Роуты
app.include_router(notifications.router, prefix='/api/v1/notifications', tags=['notifications'])
# app.include_router(roles.router, prefix='/api/v1/roles', tags=['roles'])


