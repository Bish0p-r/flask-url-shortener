from flask import flash, redirect, render_template, url_for, abort
from flask_login import current_user

from app.shortener import shortener_bp as bp
from app.shortener.models import Url
from app.shortener.forms import UrlForm
from app import db


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = UrlForm()

    if form.validate_on_submit():
        original_url = form.url.data
        url = Url(original_url=original_url)

        db.session.add(url)
        db.session.commit()

        shorted_url = url_for('shortener.url_redirect', short_url=url.short_url, _external=True)

        return render_template('shortener/index.html', form=form, shorted_url=shorted_url, user=current_user)
    return render_template('shortener/index.html', form=form, user=current_user)


@bp.route('/<short_url>')
def url_redirect(short_url):
    # pLTalw
    url = Url.query.filter_by(short_url=short_url).first()
    if url:
        return redirect(url.original_url)
    abort(404)


@bp.route('/redirect_checker', methods=['GET', 'POST'])
def redirect_checker():
    form = UrlForm()

    return render_template('shortener/redirect_checker.html', form=form, user=current_user)



