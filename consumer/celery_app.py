from celery import Celery
from celery import shared_task

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

celery_app = Celery('task', broker='pyamqp://guest@rabbitmq:5672//')


@shared_task
def send_email(recipient, subject, body_text):
    msg = MIMEMultipart()
    msg['From'] = "rmqapp@gmail.com"
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body_text, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login("rmqapp@gmail.com", "cbtjvhsalfpnopfu")
            server.sendmail("rmqapp@gmail.com", recipient, msg.as_string())
            print(f"Email sent to {recipient} successfully")
    except Exception as e:
        print(f"Error sending email: {e}")
        
        
# celery -A celery_app worker --loglevel=info
