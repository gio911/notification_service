from celery import Celery
from celery import shared_task
import httpx
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

celery_app = Celery('task', broker='pyamqp://guest@rabbitmq:5672//')


@shared_task
def transfer_to_auth_service(user_id, token):
    print(user_id, token,  39393)
    data = {"user_id":user_id, "token":token}
    # process_data.apply_async(args=[data])
    headers = {
        "Authorization": data.get("token"),  # Пример токена для авторизации
        "Content-Type": "application/json"  # Тип содержимого
    }
    user_data={"user_id":data.get("user_id")}
    print(user_data, 9999)
    with httpx.Client() as client:
        response = client.post("http://auth:8001/api/v1/users/get_user_data", json={"user_id":data.get("user_id")}, headers=headers)

        if response.status_code == 200:
            print("Successfully sent data to the other service")
        else:
            print("Failed to send data to the other service")

@shared_task      
def transfer_to_deliver_service(first_name, email):
    """
    Here we will be sent the message to mail deliver service
    """
    user_data = {"first_name":first_name, "email":email}
    print(first_name, email, 98393)
    headers = {
        "Content-Type": "application/json"
    }
    
    with httpx.Client() as client:
        response = client.post("http://email_deliver_service:8003/api/v1/email_creation/create_email", 
                               json={"first_name":user_data.get("first_name"), "email":user_data.get("email")}, 
                               headers=headers)

        if response.status_code == 200:
            print("Successfully sent data to the Message Former service")
        else:
            print("Failed to send data to the Message Former service")
    
   
# @shared_task
# def process_data(data):
#     print(33292929)
#     headers = {
#         "Authorization": data.get("token"),  # Пример токена для авторизации
#         "Content-Type": "application/json"  # Тип содержимого
#     }
#     user_data={"user_id":data.get("user_id")}
#     print(user_data, 9999)
#     with httpx.Client() as client:
#         response = client.post("http://auth:8001/api/v1/users", json={"user_id":data.get("user_id")}, headers=headers)

#         if response.status_code == 200:
#             print("Successfully sent data to the other service")
#         else:
#             print("Failed to send data to the other service")    


# celery -A celery_app worker --loglevel=info



    # msg = MIMEMultipart()
    # msg['From'] = "rmqapp@gmail.com"
    # msg['To'] = recipient
    # msg['Subject'] = subject
    # msg.attach(MIMEText(body_text, 'plain'))

    # try:
    #     with smtplib.SMTP('smtp.gmail.com', 587) as server:
    #         server.starttls()
    #         server.login("rmqapp@gmail.com", "cbtjvhsalfpnopfu")
    #         server.sendmail("rmqapp@gmail.com", recipient, msg.as_string())
    #         print(f"Email sent to {recipient} successfully")
    # except Exception as e:
    #     print(f"Error sending email: {e}")
    