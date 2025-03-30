from fastapi import APIRouter, Depends, Body, Header

from src.services.producer import Producer
from src.services.producer import get_rmq_publisher_service
from src.schemas.user_data import UserDataForEmail

router = APIRouter()


@router.post('/create_email', response_model=UserDataForEmail)
async def create_email_for_transfer(
    user_data:UserDataForEmail,
    rmq_publisher_service:Producer=Depends(get_rmq_publisher_service)):
    print(type(user_data), 123000)
    print(user_data.model_dump(), 123000)
    return user_data
    # message = {"user_id":user.user_id, "token":authorization}
    # await rmq_publisher_service.send_to_queue(message=message, routing_key="user.info")
    # return {"message":"Email queued"}



