from pydantic_settings import BaseSettings, SettingsConfigDict

    
from pathlib import Path
from logging import config as logging_config

from pydantic import Field, SecretStr
from dotenv import load_dotenv

# from src.core.logger import LOGGING

# logging_config.dictConfig(LOGGING)

BASE_DIR = Path(__file__).parent.parent.parent

class Settings(BaseSettings):
    # POSTGRESQL
    pg_username: str = Field('postgres', validation_alias='PG_USER_NAME')
    pg_password: str = Field('secret', validation_alias='PG_PASSWORD')
    pg_host: str = Field('127.0.0.1', validation_alias='PG_HOST')
    pg_port: str = Field('5678', validation_alias='PG_PORT')
    pg_db_name: str = Field('db_name', validation_alias='PG_DB_NAME')
    
    # RABBITMQ
    rmq_username: str = Field('guest', validation_alias='REBITMQ_USERNAME')
    rmq_host: str = Field('127.0.0.1', validation_alias='REBITMQ_HOST')

    # CELERY_BROKER
    redis_host: str = Field('127.0.0.1', validation_alias='REDIS_HOST')
    redis_port: str = Field('6379', validation_alias='REDIS_PORT')
    

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )


    @property
    def postgres_url(self) -> str:
        """Формируем URL для подключения к Postgres."""
        return f'postgresql+asyncpg://{self.pg_username}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db_name}'


    @property
    def rabbitmq_url(self) -> str:
        """Формируем URL для подключения к RebitMQ."""
        return f'pyamqp://{self.rmq_username}@{self.rmq_host}//'


    @property
    def redis_broker_url(self) -> str:
        """Формируем URL для подключения к Redis."""
        return f'redis://{self.redis_host}@{self.redis_port}/0'

        
    @property
    def redis_backend_url(self) -> str:
        """Формируем URL для подключения к Redis."""
        return f'redis://{self.redis_host}@{self.redis_port}/0'



settings = Settings()