from flask import url_for
from flask_mail import Message

from app import mail
from config import Config


def send_password_reset_email(user):
    token = user.get_reset_token()
    url = url_for('user.reset_password_token', token=token, _external=True)

    message = Message(
        'Password reset',
        sender=Config.MAIL_USERNAME,
        recipients=[user.email]
    )

    message.body = f"Click on the link below to change your password:\n\n{url}"

    mail.send(message)
