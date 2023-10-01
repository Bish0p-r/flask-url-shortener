from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_mail import Mail

from config import Config
from app.utils import register_handlers
from app.utils import make_celery


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap5()
login_manager = LoginManager()
mail = Mail()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    bootstrap.init_app(app)

    login_manager.init_app(app)

    mail.init_app(app)

    from app.user.tasks import test_task, send_password_reset_email
    celery = make_celery(app)
    celery.conf.update(app.config)

    app.app_context().push()
    register_handlers(app)

    from app.shortener import shortener_bp
    from app.user import user_bp

    app.register_blueprint(shortener_bp)
    app.register_blueprint(user_bp, url_prefix='/user')

    return app, celery


app, celery = create_app()
app.app_context().push()
