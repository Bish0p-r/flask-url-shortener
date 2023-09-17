from flask import flash, redirect, render_template, url_for

from app.shortener import shortener_bp as bp
from app.shortener.models import Url
from app.shortener.forms import UrlForm


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = UrlForm()

    if form.validate_on_submit():
        url = form.url.data
        # url = Url.create(url)

        # flash(f'Shortened URL: {url.short_url}', 'success')
        return render_template('index.html', form=form)

    return render_template('index.html', form=form)


@bp.route('/about')
def about():
    return "123"
