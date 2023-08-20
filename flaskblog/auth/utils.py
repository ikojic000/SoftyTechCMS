import re
from wtforms.validators import (
    ValidationError,
)
from flaskblog.models import User
from flask_login import current_user

from flaskblog.users.utils import user_has_role


# Function for checking if username is taken when new user registers
def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
        raise ValidationError("That username is taken. Please choose a different one!")


# Function for checking if email is taken when new user registers
def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError("That email is taken. Please choose a different one!")


# Function for checking if username is taken when user updates username
def validate_username_update(self, username):
    if username.data != current_user.username:
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is already taken. Please choose another one!"
            )


# Function for checking if email is taken when user updates email
def validate_email_update(self, email):
    if email.data != current_user.email:
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "That email is already taken. Please choose another one!"
            )


# Function for checking if password is valid when user registers / updates password
def validate_password(form, field):
    # Check if the password has at least 5 characters
    if len(field.data) < 5:
        raise ValidationError("Password must have at least 5 characters.")

    # Check if the password contains at least 1 uppercase letter
    if not re.search(r"[A-Z]", field.data):
        raise ValidationError("Password must contain at least 1 uppercase letter.")

    # Check if the password contains at least 1 number
    if not re.search(r"[0-9]", field.data):
        raise ValidationError("Password must contain at least 1 number.")


# Utility method for FileManager access
def accessControl_function():
    if current_user.is_authenticated:
        if user_has_role(current_user, "Admin") or user_has_role(
            current_user, "Superuser"
        ):
            return True
        else:
            return False
    else:
        return False
