import json

from flask import url_for
from datetime import datetime
from flask_jwt_extended import create_access_token

from app.user.models import User
from app.shortener.models import Url


def test_shortener_post(client, user):
    response = client.get(url_for("api.url_shortener_url_shortener"))

    assert response.status_code == 405

    response = client.post(
        url_for("api.url_shortener_url_shortener"),
        json={"original_url": "https://google.com"},
    )
    data = json.loads(response.data.decode())
    url = Url.query.filter_by(original_url="https://google.com").first()

    assert response.status_code == 201
    assert data["original_url"] == url.original_url
    assert data["visits"] == url.visits
    assert data["short_url"] == url.short_url
    assert data["active"] == url.active
    assert datetime.fromisoformat(data["created_at"]) == url.created_at

    response = client.post(
        url_for("api.url_shortener_url_shortener"),
        json={"original_url": "https://testurl.com"},
        headers={"Authorization": f"Bearer {create_access_token(user)}"},
    )

    data = json.loads(response.data.decode())
    url = Url.query.filter_by(original_url="https://testurl.com").first()

    assert response.status_code == 201
    assert data["original_url"] == url.original_url
    assert data["visits"] == url.visits
    assert data["short_url"] == url.short_url
    assert data["active"] == url.active
    assert datetime.fromisoformat(data["created_at"]) == url.created_at
    assert url in user.urls


def test_auth_post(client):
    request_data = {
        "email": "test@test.com",
        "password1": "testtest",
        "password2": "wrongpassword",
    }
    response = client.post(url_for("api.auth_register"), json=request_data)

    assert response.status_code == 400
    assert b"Passwords don't match" in response.data

    request_data = {
        "email": "test@test.com",
        "password1": "testtest",
        "password2": "testtest",
    }
    response = client.post(url_for("api.auth_register"), json=request_data)
    data = json.loads(response.data.decode())

    assert response.status_code == 201
    assert data["email"] == request_data["email"]
    assert User.query.filter_by(email=request_data["email"]).first()

    response = client.post(url_for("api.auth_register"), json=request_data)

    assert response.status_code == 400
    assert b"User already exists" in response.data

    response = client.post(
        url_for("api.auth_login"),
        json={"email": "test@test.com", "password": "wrongpassword"},
    )

    assert response.status_code == 400
    assert b"Invalid email or password" in response.data

    response = client.post(
        url_for("api.auth_login"),
        json={"email": "test@test.com", "password": "testtest"},
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert data["access_token"]
