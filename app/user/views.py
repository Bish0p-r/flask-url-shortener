from flask import flash, redirect, render_template, url_for

from app.user import user_bp as bp


@bp.route('/')
def index():
    return render_template('user/profile.html')


@bp.route('/list_of_urls')
def links_list():
    return render_template('user/list_of_urls.html')


@bp.route('/login')
def login():
    return render_template('user/login.html')
