from fastapi import APIRouter, Depends

from src.services.producer import Producer
from src.services.producer import get_rmq_publisher_service


router = APIRouter()


@router.post('/send_mail')
async def send_mail(recipient: str, subject:str, body: str, rmq_publisher_service:Producer=Depends(get_rmq_publisher_service)):
    message = {"recipient":recipient, "subject":subject, "body":body}
    await rmq_publisher_service.send_to_queue(message=message, routing_key="email.send")
    return {"message":"Email queued"}
