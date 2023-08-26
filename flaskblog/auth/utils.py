import re
from wtforms.validators import ValidationError
from flask_login import current_user
from flaskblog.users.database_manager import get_user_by_email, get_user_by_username
from flaskblog.users.utils import user_has_role


# Function for checking if username is taken when a new user registers
def validate_username(self, username):
    """
    Validate the username when a new user registers.

    Args:
        self: The form instance.
        username: The username entered by the user.

    Raises:
        ValidationError: If the username is already taken.
    """
    user = get_user_by_username(username.data)
    if user:
        raise ValidationError("That username is taken. Please choose a different one!")


# Function for checking if email is taken when a new user registers
def validate_email(self, email):
    """
    Validate the email address when a new user registers.

    Args:
        self: The form instance.
        email: The email address entered by the user.

    Raises:
        ValidationError: If the email address is already taken.
    """
    user = get_user_by_email(email.data)
    if user:
        raise ValidationError("That email is taken. Please choose a different one!")


# Function for checking if username is taken when a user updates their username
def validate_username_update(form, username):
    """
    Validate the username when a user updates their username.

    Args:
        form: The form instance.
        username: The updated username.

    Raises:
        ValidationError: If the updated username is already taken.
    """
    if username.data != current_user.username:
        user = get_user_by_username(username.data)
        if user:
            raise ValidationError(
                "That username is already taken. Please choose another one!"
            )


# Function for checking if email is taken when a user updates their email address
def validate_email_update(form, email):
    """
    Validate the email address when a user updates their email.

    Args:
        form: The form instance.
        email: The updated email address.

    Raises:
        ValidationError: If the updated email address is already taken.
    """
    if email.data != current_user.email:
        user = get_user_by_email(email.data)
        if user:
            raise ValidationError(
                "That email is already taken. Please choose another one!"
            )


# Function for checking if password is valid when a user registers or updates their password
def validate_password(form, field):
    """
    Validate the password when a user registers or updates their password.

    Args:
        form: The form instance.
        field: The password field.

    Raises:
        ValidationError: If the password does not meet the specified criteria.
    """
    # Check if the password has at least 5 characters
    if len(field.data) < 5:
        raise ValidationError("Password must have at least 5 characters.")

    # Check if the password contains at least 1 uppercase letter
    if not re.search(r"[A-Z]", field.data):
        raise ValidationError("Password must contain at least 1 uppercase letter.")

    # Check if the password contains at least 1 number
    if not re.search(r"[0-9]", field.data):
        raise ValidationError("Password must contain at least 1 number.")


# Utility function for FileManager access control
def accessControl_function():
    """
    Determine if the current user has access to the FileManager.

    Returns:
        bool: True if the user has access, False otherwise.
    """
    if current_user.is_authenticated:
        if user_has_role(current_user, "Admin") or user_has_role(
            current_user, "Superuser"
        ):
            return True
        else:
            return False
    else:
        return False
