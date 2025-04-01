from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.db import rmq
from src.api.endpoints import notifications
import aio_pika
from src.core.config import settings

# Создаем экземпляр FastAPI
@asynccontextmanager
async def lifespan(_: FastAPI):

    rmq.rabbitmq_connection = await aio_pika.connect_robust(
        f'amqp://{settings.rmq_user}:{settings.rmq_password}@{settings.rmq_host}:5672/'
    )

    yield

    await rmq.rabbitmq_connection.close()


# Один экземпляр FastAPI
app = FastAPI(
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

# Роуты
app.include_router(
    notifications.router,
    prefix='/api/v1/notifications',
    tags=['notifications'],
)
