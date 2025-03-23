from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from src.core.config import settings  # Загружаем настройки

Base = declarative_base()

# Формируем DSN строку для подключения к БД
dsn = settings.postgres_url

echo_setting = os.getenv("SQLALCHEMY_ECHO", "False") in ["True"]

# Создаём асинхронный движок
engine = create_async_engine(dsn, echo=echo_setting, future=True)

# Создаём фабрику сессий
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
