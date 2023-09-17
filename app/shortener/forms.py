from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, Length


class UrlForm(FlaskForm):
    url = URLField('URL', validators=[URL(), Length(max=512)])
    submit = SubmitField('Shorten')
