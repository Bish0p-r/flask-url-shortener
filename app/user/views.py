from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.user import user_bp as bp
from app.user.models import User
from app.user.forms import LoginForm, RegisterForm
from app import db


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash_password = generate_password_hash(form.password2.data)
        new_user = User(email=form.email.data, password=hash_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form, user=current_user)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)

    return render_template('user/login.html', form=form, user=current_user)


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('shortener.index'))


@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('user/profile.html', user=current_user)


@bp.route('/list_of_urls')
def links_list():
    return render_template('user/list_of_urls.html', user=current_user)
