from app import db
import random
import string


class Url(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(100))
    short_url = db.Column(db.String(6), unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    visits = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    relationships = db.relationship('User', backref='urls')

    def __repr__(self):
        return f"<Url: {self.id}>"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.short_url = self.generate_short_url()

    def generate_short_url(self):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if Url.query.filter_by(short_url=random_string).first():
            return self.generate_short_url()
        return random_string
