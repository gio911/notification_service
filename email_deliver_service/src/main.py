from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.db import rmq
from src.api.endpoints import transfer_email
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

#Роуты
app.include_router(transfer_email.router, prefix='/api/v1/email_creation', tags=['email_creation'])


