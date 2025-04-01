from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.core.config import settings

from src.api.v1 import users
from src.core.logging_config import setup_logging

from fastapi.responses import JSONResponse
from src.db import rmq
import aio_pika

logger = setup_logging()

import logging

# Создаем экземпляр FastAPI
@asynccontextmanager
async def lifespan(_: FastAPI):

    rmq.rabbitmq_connection = await aio_pika.connect_robust(
        'amqp://guest:guest@rabbitmq:5672/'
    )

    yield

    # Закрытие соединений при завершении работы
    await rmq.rabbitmq_connection.close()


# Один экземпляр FastAPI
app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    redirect_slashes=False,
)

# Логирование
logger.info('Логгер настроен!')

# Роуты
app.include_router(users.router, prefix='/api/v1/users', tags=['users'])
