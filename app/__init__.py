from flask import Flask

from config import Config
from app.utils import register_handlers
from app.utils import make_celery
from app.extensions import db, migrate, bootstrap, login_manager, mail, jwt, api
from app.api.views import ns
from app.user.models import User


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    jwt.init_app(app)

    migrate.init_app(app, db, render_as_batch=True)

    bootstrap.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "user.login"

    mail.init_app(app)

    from app.user.tasks import test_task, send_password_reset_email

    celery = make_celery(app)
    celery.conf.update(app.config)

    app.app_context().push()
    register_handlers(app)

    from app.shortener import shortener_bp
    from app.user import user_bp
    from app.extensions import api_bp

    app.register_blueprint(shortener_bp)
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(api_bp)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).first()

    return app, celery


app, celery = create_app()
app.app_context().push()
