from flask_login import UserMixin

from app import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(256), nullable=False)

    # url_id = db.Column(db.Integer, db.ForeignKey('urls.id'), nullable=True)
    # relationships = db.relationship('Url', backref='user')

    def __repr__(self):
        return f"<User: {self.email}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
