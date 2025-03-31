from ..core.config import settings
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os
# Создаём базовый класс для будущих моделей
Base = declarative_base()
# Создаём движок
# Настройки подключения к БД передаём из переменных окружения, которые заранее загружены в файл настроек
dsn = f'postgresql+asyncpg://{settings.user}:{settings.password}@{settings.host}:{settings.port}/{settings.db}'


echo_setting = os.getenv("SQLALCHEMY_ECHO", "False") in ["True"]

engine = create_async_engine(dsn, echo=echo_setting, future=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)  
  
    
async def get_session() -> AsyncSession:
   async with async_session() as session:
       try:
           yield session
       except Exception:
           await session.rollback()
           raise
       finally:
           await session.close()
           
        
async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def purge_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)