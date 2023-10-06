from flask import Blueprint
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap5()
login_manager = LoginManager()
mail = Mail()
jwt = JWTManager()

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(api_bp, doc="/doc")
