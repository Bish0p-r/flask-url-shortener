from datetime import timedelta, datetime

from flask_login import UserMixin
from authlib.jose import jwt

from app import db, login_manager
from config import Config


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(256), nullable=False)

    def get_reset_token(self):
        secret_key = Config.SECRET_KEY
        expires_in = timedelta(minutes=30)
        issued_at = datetime.now()
        expires_at = issued_at + expires_in

        header = {"alg": "HS256", "typ": "JWT"}
        payload = {"user_id": self.id, "exp": expires_at.timestamp(), "iat": issued_at}
        token = jwt.encode(header, payload, secret_key)

        return token

    @staticmethod
    def verify_reset_token(token):
        try:
            decoded_payload = jwt.decode(token, Config.SECRET_KEY)
            expires_at = datetime.fromtimestamp(decoded_payload["exp"])

            if expires_at <= datetime.now():
                return None
            return User.query.get(decoded_payload["user_id"])

        except:
            return None

    def __repr__(self):
        return f"<User: {self.email}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
