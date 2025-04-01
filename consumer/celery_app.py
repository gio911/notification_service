from celery import Celery
from celery import shared_task
import httpx
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from config.logging_config import setup_logging
from config.config import settings

logger = setup_logging()

celery_app = Celery(
    'task',
    broker=f'pyamqp://{settings.rmq_user}:{settings.rmq_password}@{settings.rmq_host}:5672//',
)


@shared_task
def transfer_to_auth_service(user_id, token):
    logger.info(f'Обрабатываем пользователя {user_id} с токеном {token}')
    data = {'user_id': user_id, 'token': token}
    headers = {
        'Authorization': data.get('token'),
        'Content-Type': 'application/json',
    }
    user_data = {'user_id': data.get('user_id')}
    logger.debug(f'Данные пользователя: {user_data}')

    with httpx.Client() as client:
        try:
            response = client.post(
                'http://auth:8001/api/v1/users/get_user_data',
                json={'user_id': data.get('user_id')},
                headers=headers,
            )
            if response.status_code == 200:
                logger.info('Данные успешно отправлены в другой сервис')
            else:
                logger.error(
                    f'Не удалось отправить данные в другой сервис, код статуса: {response.status_code}'
                )
        except httpx.RequestError as e:
            logger.error(f'Ошибка запроса: {e}')


@shared_task
def transfer_to_deliver_service(first_name, email):
    """Отправляем сообщение в сервис доставки писем"""
    user_data = {'first_name': first_name, 'email': email}
    logger.info(f'Обрабатываем email для {first_name} ({email})')
    headers = {'Content-Type': 'application/json'}

    with httpx.Client() as client:
        try:
            response = client.post(
                'http://email_deliver_service:8003/api/v1/email_creation/create_email',
                json={
                    'first_name': user_data.get('first_name'),
                    'email': user_data.get('email'),
                },
                headers=headers,
            )

            if response.status_code == 200:
                logger.info(
                    'Данные успешно отправлены в сервис формирования сообщений'
                )
            else:
                logger.error(
                    f'Не удалось отправить данные в сервис формирования сообщений, код статуса: {response.status_code}'
                )
        except httpx.RequestError as e:
            logger.error(f'Ошибка запроса: {e}')


@shared_task
def send_email(to_email, first_name):
    """Отправка письма (фейковая отправка письма в этом примере)"""
    body_text = generate_email(to_email, first_name)
    # Создание MIME-сообщения
    msg = MIMEMultipart()
    msg['From'] = 'rmqapp@gmail.com'
    msg['To'] = to_email
    msg['Subject'] = 'Новая новинка в онлайн кинотеатре!'

    # Тело письма в HTML формате
    msg.attach(MIMEText(body_text, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Начинаем защищенное соединение
            server.login(
                'rmqapp@gmail.com', 'cbtjvhsalfpnopfu'
            )  # Логин и пароль

            server.sendmail('rmqapp@gmail.com', to_email, msg.as_string())
            logger.info(f'Письмо успешно отправлено на {to_email}')

    except Exception as e:
        logger.error(f'Ошибка при отправке письма: {e}')
    logger.info(f'Отправлено письмо на {to_email}: {first_name}')


def generate_email(email, first_name):
    email_template = """
    <html>
        <body>
            <p>Здравствуйте, {{ first_name }}!</p>
            <p>Мы рады сообщить вам, что в нашем онлайн кинотеатре появилась новинка</p>
            <p>Не пропустите возможность посмотреть его первым.</p>
            <p>Ваш email: {{ email }}</p>
            <p>Наслаждайтесь просмотром!</p>
            <p>С уважением, команда онлайн кинотеатра.</p>
        </body>
    </html>
    """

    template = Template(email_template)

    email_content = template.render(first_name=first_name, email=email)

    return email_content


@shared_task
def send_email(to_email, first_name):
    """Отправка письма"""
    body_text = generate_email(to_email, first_name)
    # Создание MIME-сообщения
    msg = MIMEMultipart()
    msg['From'] = 'rmqapp@gmail.com'
    msg['To'] = to_email
    msg['Subject'] = 'Новая новинка в онлайн кинотеатре!'

    # Тело письма в HTML формате
    msg.attach(MIMEText(body_text, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Начинаем защищенное соединение
            server.login(
                'rmqapp@gmail.com', 'cbtjvhsalfpnopfu'
            )  # Логин и пароль

            server.sendmail('rmqapp@gmail.com', to_email, msg.as_string())
            logger.info(f'Письмо успешно отправлено на {to_email}')

    except Exception as e:
        logger.error(f'Ошибка при отправке письма: {e}')
    logger.info(f'Отправлено письмо на {to_email}: {first_name}')


def generate_email_for_register(user_name, user_email):
    email_template = """
    <html>
        <body>
            <p>Здравствуйте, {{ user_name }}!</p>
            <p>Вы зарегистрированы в сервисе</p>
            
            <p>Ваш email: {{ user_email }}</p>
            <p>Наслаждайтесь нашим онлайн кинотеатром!</p>
            <p>С уважением, команда онлайн кинотеатра.</p>
        </body>
    </html>
    """

    template = Template(email_template)

    email_content = template.render(first_name=user_name, email=user_email)

    return email_content


@shared_task
def send_email_for_register_user(user_name, user_email):
    """Отправка письма"""
    body_text = generate_email_for_register(user_name, user_email)
    # Создание MIME-сообщения
    msg = MIMEMultipart()
    msg['From'] = 'rmqapp@gmail.com'
    msg['To'] = user_email
    msg['Subject'] = 'Новая новинка в онлайн кинотеатре!'

    # Тело письма в HTML формате
    msg.attach(MIMEText(body_text, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Начинаем защищенное соединение
            server.login(
                'rmqapp@gmail.com', 'cbtjvhsalfpnopfu'
            )  # Логин и пароль

            server.sendmail('rmqapp@gmail.com', user_email, msg.as_string())
            logger.info(f'Письмо успешно отправлено на {user_email}')

    except Exception as e:
        logger.error(f'Ошибка при отправке письма: {e}')
    logger.info(f'Отправлено письмо на {user_email}: {user_name}')
