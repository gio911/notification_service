
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery_conf import celery_app

import smtplib



@celery_app.task(name="tasks.email.send_email")
def send_email(data):
    print(data, 94848484)
    print(f"Получено сообщение для отправки email: {data}")
    
    recipient = data['recipient']
    subject = data['subject']
    body_text = data['body']
    
    
    msg=MIMEMultipart()
    msg['From'] = "rmqapp@gmail.com"
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body_text, 'plain'))
    # celery -A celery_conf inspect registered

    # Отправка письма
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login("rmqapp@gmail.com", "cbtjvhsalfpnopfu")
            server.sendmail("rmqapp@gmail.com", recipient, msg.as_string())
            print("Email успешно отправлен!")
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")