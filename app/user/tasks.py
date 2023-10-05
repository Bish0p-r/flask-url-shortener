from celery import shared_task
from flask import url_for
from flask_mail import Message

from app import mail
from app.user.models import User
from config import Config, host


@shared_task()
def test_task(a, b):
    print(a, b)
    return a + b


@shared_task()
def send_password_reset_email(email):
    user = User.query.filter_by(email=email).first()
    token = user.get_reset_token()
    url = f"{host}/user/reset_password/{token}"

    message = Message(
        'Password reset',
        sender=Config.MAIL_USERNAME,
        recipients=[user.email]
    )

    message.body = f"Click on the link below to change your password:\n\n{url}"

    mail.send(message)
