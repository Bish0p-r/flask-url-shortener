from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import generate_password_hash
from sqlalchemy import or_

from app.shortener.models import Url
from app.user import user_bp as bp
from app.user.models import User
from app.user.forms import (LoginForm,
                            RegisterForm,
                            ProfileForm,
                            ResetPasswordRequestForm,
                            ResetPasswordForm)
from app import db
from app.user.tasks import send_password_reset_email


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    user = current_user

    if user.is_authenticated:
        return redirect(url_for('shortener.index'))

    if form.validate_on_submit():
        hash_password = generate_password_hash(form.password2.data)
        new_user = User(email=form.email.data, password=hash_password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form, user=user, title='Registration')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = current_user

    if user.is_authenticated:
        return redirect(url_for('shortener.index'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)

        return redirect(url_for('shortener.index'))
    return render_template('user/login.html', form=form, user=user, title='Login')


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('shortener.index'))


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()

    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()

    return render_template('user/profile.html', user=current_user, form=form, title='Profile')


@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    user = current_user

    if user.is_authenticated:
        return redirect(url_for('shortener.index'))

    if form.validate_on_submit():
        send_password_reset_email.delay(form.email.data)
        flash('Check your email for the instructions to reset your password.', category='success')

        return redirect(url_for('user.login'))
    return render_template('user/reset_password_request.html', user=user, form=form, title='Reset password')


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    form = ResetPasswordForm()

    if current_user.is_authenticated:
        return redirect(url_for('shortener.index'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token', category='danger')

        return redirect(url_for('user.reset_password_request'))

    if form.validate_on_submit():
        hash_password = generate_password_hash(form.password2.data)
        user.password = hash_password

        db.session.commit()
        flash('Your password has been updated!', category='success')

        return redirect(url_for('user.login'))
    return render_template('user/reset_password.html', user=current_user, form=form, title='Reset password')


@bp.route('/list_of_urls', methods=['GET', 'POST'])
@login_required
def links_list():
    page = request.args.get('page', 1, type=int)
    form_data = request.args.get('query')

    if form_data:
        urls = Url.query.filter_by(
            user_id=current_user.id
        ).filter(
            or_(Url.original_url.ilike(f'%{form_data}%'), Url.short_url.ilike(f'%{form_data}%'))
        ).order_by(
            Url.created_at.desc()
        )
    else:
        urls = Url.query.filter_by(user_id=current_user.id).order_by(Url.created_at.desc())

    pages = urls.paginate(page=page, per_page=10)

    return render_template('user/list_of_urls.html', user=current_user, urls=urls, pages=pages, title='List of URLS')


@bp.route('/link_status/<id>', methods=['GET', 'POST'])
@login_required
def set_link_status(id):
    user = current_user
    link = Url.query.filter_by(id=id, user_id=user.id).first()
    if link:
        link.active = not link.active
        db.session.commit()

    return redirect(url_for('user.links_list'))
