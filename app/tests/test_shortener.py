from flask import url_for
from flask_login import login_user

from app.shortener.models import Url


def test_shortener_get(client):
    response = client.get(url_for('shortener.index'))

    assert response.status_code == 200
    assert b'URL Shortener' in response.data


def test_shortener_post(client):
    response = client.post(url_for('shortener.index'), data={'url': 'https://google.com', 'submit': 'SUBMIT'})

    assert response.status_code == 200
    assert Url.query.filter_by(original_url='https://google.com').first()


def test_shortener_redirect(client):
    client.post(url_for('shortener.index'), data={'url': 'https://google.com', 'submit': 'SUBMIT'})
    url = Url.query.filter_by(original_url='https://google.com').first()

    assert url.visits == 0

    response = client.get(url.short_url)

    assert response.status_code == 302
    assert response.location == url.original_url
    assert url.visits == 1


def test_redirect_checker_get(client):
    response = client.get(url_for('shortener.redirect_checker'))

    assert response.status_code == 200


def test_redirect_checker_post(client):
    client.post(url_for('shortener.index'), data={'url': 'https://google.com', 'submit': 'SUBMIT'})

    url = Url.query.filter_by(original_url='https://google.com').first()
    response = client.post(url_for('shortener.redirect_checker'), data={'url': url.short_url, 'submit': 'SUBMIT'})

    assert response.status_code == 200
    assert b'https://google.com' in response.data


def test_shortener_user_post(client, user):
    response = client.post(url_for('shortener.index'), data={'url': 'https://google.com', 'submit': 'SUBMIT'})

    assert response.status_code == 200
    assert not Url.query.filter_by(original_url='https://google.com').first().user_id

    login_user(user)
    response = client.post(url_for('shortener.index'), data={'url': 'https://testlink.com', 'submit': 'SUBMIT'})

    assert response.status_code == 200
    assert Url.query.filter_by(original_url='https://testlink.com').first().user_id == user.id
