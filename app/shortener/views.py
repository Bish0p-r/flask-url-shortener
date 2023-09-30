import requests

from flask import flash, redirect, render_template, url_for, abort
from flask_login import current_user

from app.shortener import shortener_bp as bp
from app.shortener.models import Url
from app.shortener.forms import UrlForm
from app import db
from config import host


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = UrlForm()
    user = current_user
    shorted_url = None

    if form.validate_on_submit():
        original_url = form.url.data
        url = Url(original_url=original_url)

        if user.is_authenticated:
            user.urls.append(url)

        db.session.add(url)
        db.session.commit()

        shorted_url = url.short_url
    return render_template('shortener/index.html', form=form, shorted_url=shorted_url, user=user, title='URL Shortener')


@bp.route('/<short_url>')
def url_redirect(short_url):
    short_url = host + '/' + short_url
    url = Url.query.filter_by(short_url=short_url, active=True).first()

    if url:
        url.visits += 1
        db.session.commit()

        return redirect(url.original_url)
    abort(404)


@bp.route('/redirect_checker', methods=['GET', 'POST'])
def redirect_checker():
    form = UrlForm()
    redirect_to = None

    if form.validate_on_submit():
        url = form.url.data

        if url.startswith(host):
            q = Url.query.filter_by(short_url=url, active=True).first()
            if q:
                redirect_to = q.original_url
        else:
            response = requests.get(url, allow_redirects=False)

            if response.status_code == 301 or response.status_code == 302:
                redirect_to = response.next.url
            else:
                redirect_to = url

    return render_template(
        'shortener/redirect_checker.html',
        form=form,
        user=current_user,
        redirect_to=redirect_to,
        title='Redirect checker'
    )
