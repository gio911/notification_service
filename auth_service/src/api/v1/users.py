from fastapi import APIRouter, Depends, status, Header
from ...schemas.entity import User, UserForNotification
from src.services.users import UserService, get_user_service
from src.services.producer import get_rmq_publisher_service, Producer
from fastapi import Depends

import logging
logger = logging.getLogger(__name__)


router = APIRouter()

def serialize_sqlalchemy_object(obj):
    """Конвертирует SQLAlchemy объект в сериализуемый словарь."""
    return {column: getattr(obj, column) for column in obj.__table__.columns.keys()}


@router.post("/get_user_data", status_code=status.HTTP_200_OK, response_model=UserForNotification)
async def get_user_data(user: User,
                        authorization: str = Header(..., alias="Authorization"),
                        user_service: UserService = Depends(get_user_service),
                        producer_service: Producer = Depends(get_rmq_publisher_service)
                        ):
    """
    Эндпоинт для получения данных пользователя по user_id.
    Проверяет валидность токена в заголовке Authorization.
    """
    print(123321)
    logger.debug(f"Received user_id: {user.user_id}, authorization: {authorization}")
    print(123321)

    user_obj = await user_service.get_user_data_for_admin(user.user_id, authorization)
    print(user_obj, 83774)
    print(type(user_obj), 893774)
    # Преобразуем SQLAlchemy объект в словарь
    user_dict = serialize_sqlalchemy_object(user_obj)

    await producer_service.send_to_queue(user_dict, routing_key="mail.generate")

    return user_obj

