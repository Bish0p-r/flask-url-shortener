from flask import url_for
from flask_login import current_user, login_user

from app.shortener.models import Url
from app.user.models import User


def test_registration_login_logout(client, app):
    response = client.post(
        url_for("user.register"),
        data={
            "email": "test@mail.com",
            "password1": "passwordtest",
            "password2": "passwordtest",
            "submit": "REGISTER",
        },
    )

    assert response.status_code == 302
    assert User.query.count() == 1
    assert User.query.filter_by(email="test@mail.com").first()
    assert not current_user.is_authenticated

    response = client.post(
        url_for("user.login"),
        data={"email": "test@mail.com", "password": "passwordtest", "submit": "LOGIN"},
    )

    assert response.status_code == 302
    assert current_user.is_authenticated

    response = client.get(url_for("user.logout"))

    assert response.status_code == 302
    assert not current_user.is_authenticated


def test_profile_get(client, user):
    response = client.get(url_for("user.profile"))

    assert not current_user.is_authenticated
    assert response.status_code == 302

    login_user(user)
    response = client.get(url_for("user.profile"))

    assert response.status_code == 200


def test_profile_post(client, user):
    response = client.post(
        url_for("user.profile"),
        data={
            "first_name": "Test_Name",
            "last_name": "Test_Last_Name",
            "submit": "Save changes",
        },
    )

    assert not current_user.is_authenticated
    assert response.status_code == 302

    login_user(user)
    response = client.post(
        url_for("user.profile"),
        data={
            "email": user.email,
            "first_name": "Test_Name",
            "last_name": "Test_Last_Name",
            "submit": "Save changes",
        },
    )

    assert response.status_code == 200
    assert user.first_name == "Test_Name"
    assert user.last_name == "Test_Last_Name"


def test_list_urls(client, user):
    response = client.get(url_for("user.links_list"))

    assert not current_user.is_authenticated
    assert response.status_code == 302

    login_user(user)
    response = client.get(url_for("user.links_list"))

    assert response.status_code == 200


def test_set_link_status(client, user):
    response = client.get(url_for("user.set_link_status", id=1))

    assert not current_user.is_authenticated
    assert response.status_code == 302

    login_user(user)
    client.post(
        url_for("shortener.index"),
        data={"url": "https://testlink.com", "submit": "SUBMIT"},
    )
    url = Url.query.filter_by(original_url="https://testlink.com").first()
    response = client.get(url_for("user.set_link_status", id=url.id))

    assert response.status_code == 302
    assert not url.active
