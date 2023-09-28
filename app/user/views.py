from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.shortener.models import Url
from app.user import user_bp as bp
from app.user.models import User
from app.user.forms import LoginForm, RegisterForm, ProfileForm
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

        return redirect(url_for('shortener.index'))
    return render_template('user/login.html', form=form, user=current_user)


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

    return render_template('user/profile.html', user=current_user, form=form)


@bp.route('/list_of_urls', methods=['GET', 'POST'])
@login_required
def links_list():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        urls = Url.query.filter_by(user_id=current_user.id).order_by(Url.created_at.desc())
        pages = urls.paginate(page=page, per_page=10)

        return render_template('user/list_of_urls.html', user=current_user, urls=urls, pages=pages)
    return redirect(url_for('user.login'))


@bp.route('/link_status/<id>', methods=['GET', 'POST'])
@login_required
def set_link_status(id):
    link = Url.query.filter_by(id=id).first()
    link.active = not link.active
    db.session.commit()
    return redirect(url_for('user.links_list'))
