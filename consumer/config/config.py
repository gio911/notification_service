from pathlib import Path
from logging import config as logging_config

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent.parent

COMMON_USER_ROUTING_KEY = 'user.*'
COMMON_MAIL_ROUTING_KEY = 'mail.*'
COMMON_CREATE_ROUTING_KEY = 'create.*'
COMMON_REGISTER_ROUTING_KEY = 'register.*'
NOTIFICATION_EXCHANGE = 'notification_exchange'
NOTIFICATION_QUEUE = 'new_film_notif_queue'
MAIL_GENERATE_QUEUE = 'mail_generate'
MAIL_SEND_QUEUE = 'email_send'
USER_REGISTRATION_QUEUE = 'users_registration'


class Settings(BaseSettings):

    rmq_user: str = Field('guest', validation_alias='RABBITMQ_USERNAME')
    rmq_password: str = Field('guest', validation_alias='RABBITMQ_PASSWORD')
    rmq_host: str = Field('rabbitmq', validation_alias='RABBITMQ_HOST')
    rmq_port: str = Field('5673', validation_alias='RABBITMQ_HOST')


settings = Settings()
