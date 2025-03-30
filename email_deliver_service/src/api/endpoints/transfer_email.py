from fastapi import APIRouter, Depends, Body, Header

from src.services.producer import Producer
from src.services.producer import get_rmq_publisher_service
from src.schemas.user_data import UserDataForEmail

router = APIRouter()


@router.post('/create_email')
async def create_email_for_transfer(
    user_data:UserDataForEmail,
    rmq_publisher_service:Producer=Depends(get_rmq_publisher_service)):
    message = user_data.model_dump()
    await rmq_publisher_service.send_to_queue(message=message, routing_key="create.email")




