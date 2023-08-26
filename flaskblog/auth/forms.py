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


# Form for logging in
class LoginForm(FlaskForm):
    """
    Form for user login.

    Attributes:
        email (StringField): The email field for username or email input.
        password (PasswordField): The password field.
        submit (SubmitField): The submission button for login.
    """

    email = StringField(
        "Email",
        validators=[
            DataRequired(
                message="Username/Email is required. Please enter your username or email."
            ),
        ],
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")  # Submit button


# Form for user registration
class RegisterForm(FlaskForm):
    """
    Form for user registration.

    Attributes:
        name (StringField): The name field (optional).
        username (StringField): The username field with custom validation.
        email (StringField): The email field with custom validation.
        password (PasswordField): The password field with custom validation.
        confirm_password (PasswordField): The confirmation password field.
        submit (SubmitField): The submission button for registration.
    """

    name = StringField("Name", validators=[Length(max=50)])  # Name field (optional)
    username = StringField(
        "Username",
        validators=[
            validate_username,  # Custom username validation
            DataRequired(message="Username is required. Please enter your username."),
            Length(
                min=3,
                max=15,
                message="Username must be between 3 and 15 characters long. Please choose a different one!",
            ),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            validate_email,  # Custom email validation
            DataRequired(message="Email is required. Please enter your email."),
            Email(),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            validate_password,  # Custom password validation
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(
                message="Confirm Password is required. Please retype your password."
            ),
            EqualTo(
                "password", message="Passwords must match!"
            ),  # Check password confirmation
        ],
    )
    submit = SubmitField("Register")  # Submit button for registration
