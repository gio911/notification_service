from fastapi import APIRouter, Depends, Body, Header

from src.services.producer import Producer
from src.services.producer import get_rmq_publisher_service
from src.schemas.user import User

router = APIRouter()


@router.post('/send_new_film_notification')
async def send_new_film_notification(
    user:User,
    authorization: str = Header(None, alias='Authorization'),
    rmq_publisher_service:Producer=Depends(get_rmq_publisher_service)):
    message = {"user_id":user.user_id, "token":authorization}
    await rmq_publisher_service.send_to_queue(message=message, routing_key="user.info")
    return {"message":"Email queued"}



