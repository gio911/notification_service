from pydantic_settings import BaseSettings

from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):

    rmq_user:str = Field('guest', validation_alias='RABBITMQ_USERNAME')
    rmq_password:str = Field('guest', validation_alias='RABBITMQ_PASSWORD')
    rmq_host:str = Field('rabbitmq', validation_alias='RABBITMQ_HOST')
    rmq_port:str = Field(5673, validation_alias='RABBITMQ_HOST')


settings = Settings()