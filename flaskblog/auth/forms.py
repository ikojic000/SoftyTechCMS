from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
)
from flaskblog.auth.utils import validate_email, validate_password, validate_username


# Form for loging in
class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
        ],
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


# Form for registration
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[Length(min=2, max=50)])
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=15), validate_username],
    )
    email = StringField("Email", validators=[DataRequired(), Email(), validate_email])
    password = PasswordField("Password", validators=[DataRequired(), validate_password])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")
