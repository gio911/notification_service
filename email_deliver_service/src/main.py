from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.db import rmq
from src.api.endpoints import transfer_email
import aio_pika
from core.config import settings


# Создаем экземпляр FastAPI
@asynccontextmanager
async def lifespan(_: FastAPI):
    
    rmq.rabbitmq_connection = await aio_pika.connect_robust(f"amqp://{settings.rmq_user}:{settings.rmq_password}@{settings.rmq_host}:{settings.rmq_port}/")
    
    yield

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


