from pathlib import Path
from logging import config as logging_config

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):

    project_name: str = Field('auth', validation_alias='PROJECT_NAME')

    user:str = Field('postgres', validation_alias='POSTGRES_USER')
    password:str = Field('db_password', validation_alias='POSTGRES_PASSWORD')
    host:str = Field('127.0.0.1', validation_alias='POSTGRES_HOST')
    port:int=Field(5432, validation_alias='POSTGRES_PORT')
    db:str=Field('auth_db', validation_alias='POSTGRES_DB_AUTH')
    
    
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / 'auth_service' / '.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()
