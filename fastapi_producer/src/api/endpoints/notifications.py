from fastapi import APIRouter, Depends, Body, Header

from src.services.producer import Producer
from src.services.producer import get_rmq_publisher_service
from src.schemas.user import User, NewUser
from src.core.config import REGISTER_USER_RK, USER_INFO_RK

router = APIRouter()


@router.post('/send_new_film_notification')
async def send_new_film_notification(
    user: User,
    authorization: str = Header(None, alias='Authorization'),
    rmq_publisher_service: Producer = Depends(get_rmq_publisher_service),
):
    message = {'user_id': user.user_id, 'token': authorization}
    await rmq_publisher_service.send_to_queue(
        message=message, routing_key=USER_INFO_RK
    )
    return {'message': 'Email queued'}


@router.post('/register')
async def register(
    new_user: NewUser,
    rmq_publisher_service: Producer = Depends(get_rmq_publisher_service),
):
    message = {'name': new_user.name, 'email': new_user.email}
    await rmq_publisher_service.send_to_queue(
        message=message, routing_key=REGISTER_USER_RK
    )
    return {'message': 'Message queued'}
