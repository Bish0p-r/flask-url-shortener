from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, Length


class UrlForm(FlaskForm):
    url = URLField(
        label="",
        validators=[URL(), Length(max=512)],
        render_kw={"placeholder": "Enter your URL"},
    )
    submit = SubmitField("SUBMIT")
