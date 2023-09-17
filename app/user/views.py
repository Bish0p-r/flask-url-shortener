from flask import flash, redirect, render_template, url_for

from app.user import user_bp as bp


@bp.route('/')
def index():
    return f"USER INDEX"


@bp.route('/<username>')
def user(username):
    return f"USER {username}"
