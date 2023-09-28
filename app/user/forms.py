from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField, EmailField, PasswordField, ValidationError
from wtforms.validators import URL, Length, Email, InputRequired
from werkzeug.security import check_password_hash

from app.user.models import User


class LoginForm(FlaskForm):
    email = EmailField(
        label="",
        validators=[Email(), Length(max=128), InputRequired()],
        render_kw={'placeholder': "Email"}
    )
    password = PasswordField(
        label="",
        validators=[Length(max=256), InputRequired()],
        render_kw={'placeholder': "Password"}
    )
    submit = SubmitField('LOGIN')

    def validate(self, extra_validators=None):
        rv = FlaskForm.validate(self)
        if rv:
            user = User.query.filter_by(email=self.email.data).first()
            if not user or not check_password_hash(user.password, self.password.data):
                self.email.errors.append("Wrong password or e-mail")
                self.password.errors.append("Wrong password or e-mail")
                return False
            return True
        return False


class RegisterForm(FlaskForm):
    email = EmailField(
        label="",
        validators=[Email(), Length(max=128), InputRequired()],
        render_kw={'placeholder': "Email"}
    )
    password1 = PasswordField(
        label="",
        validators=[Length(min=8), Length(max=256), InputRequired()],
        render_kw={'placeholder': "Password"}
    )
    password2 = PasswordField(
        label="",
        validators=[Length(min=8), Length(max=256), InputRequired()],
        render_kw={'placeholder': "Reenter the password"}
    )
    submit = SubmitField('REGISTER')

    def validate_password2(self, password2):
        if self.password1.data != password2.data:
            raise ValidationError("Passwords don't match")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("This e-mail address is already taken")


class ProfileForm(FlaskForm):
    email = EmailField(
        label="Email",
        validators=[Email(), Length(max=128)],
        render_kw={'placeholder': "Email"}
    )
    first_name = StringField(
        label="First name",
        validators=[Length(max=64)],
        render_kw={'placeholder': "First name"}
    )
    last_name = StringField(
        label="Last name",
        validators=[Length(max=64)],
        render_kw={'placeholder': "Last name"}
    )
    submit = SubmitField('Save changes')
