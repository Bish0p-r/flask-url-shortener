from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5

from config import Config


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap5()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    bootstrap.init_app(app)

    from app.shortener import shortener_bp
    from app.user import user_bp

    app.register_blueprint(shortener_bp)
    app.register_blueprint(user_bp, url_prefix='/user')

    return app
