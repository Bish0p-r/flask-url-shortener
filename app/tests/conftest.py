import pytest
import os
import tempfile

from app import create_app, db
from config import TestingConfig
from app.user.models import User


@pytest.fixture()
def app():
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)

    app, celery = create_app(config=TestingConfig)
    app_context = app.test_request_context()
    app_context.push()

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

    os.unlink(db_path)


@pytest.fixture()
def user(app):
    user = User(email='user@mail.com', password='passworduser')
    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture()
def client(app):
    return app.test_client()


