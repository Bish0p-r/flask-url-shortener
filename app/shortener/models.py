from app import db


class Url(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(100))
    short_url = db.Column(db.String(10))

    def __repr__(self):
        return f"<Url: {self.id}>"
