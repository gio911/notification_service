from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.core.config import settings

from src.api.v1 import users
from .logger import setup_logging

from fastapi.responses import JSONResponse
from src.db import rmq
import aio_pika
setup_logging()

import logging

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
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    redirect_slashes=False
)

# Логирование
logger = logging.getLogger("app")
logger.info("Логгер настроен!")
logger.debug("Это сообщение DEBUG.")


# Роуты
app.include_router(users.router, prefix='/api/v1/users', tags=['users'])
