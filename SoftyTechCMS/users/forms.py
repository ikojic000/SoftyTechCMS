from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    SubmitField,
    RadioField,
    SelectMultipleField,
    PasswordField,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo
from SoftyTechCMS.auth.utils import (
    validate_email,
    validate_email_update,
    validate_password,
    validate_username,
    validate_username_update,
)
from SoftyTechCMS.models import Role


# Form for updating user account
class UpdateAccountForm(FlaskForm):
    """
    A FlaskForm class for updating a user's account information.

    Attributes:
        username (StringField): Field to display and edit the username.
        email (StringField): Field to display and edit the email.
        role (RadioField): Radio button field for selecting a user's role.
        active (BooleanField): Checkbox field for user's active status.
        submit (SubmitField): Button to submit the form.
    """

    username = StringField(
        "Username",
        render_kw={"readonly": True},  # Make the field readonly
    )
    email = StringField(
        "Email",
        validators=[Email(), validate_email_update],
        render_kw={"readonly": True},  # Make the field readonly
    )
    # Fetch all roles and create choices from role names
    role_choices = [(role.id, role.name) for role in Role.query.all()]
    role = RadioField(
        "Role",
        choices=role_choices,
        validators=[DataRequired()],
    )
    active = BooleanField("Active")  # Checkbox for active field
    submit = SubmitField("Update")


# Form for Changing user settings - Role & Active
class UserRoleForm(FlaskForm):
    """
    A FlaskForm class for changing a user's role and active status.

    Attributes:
        username (StringField): Field to display the username.
        email (StringField): Field to display the email.
        role (SelectMultipleField): Multi-select field for changing user roles.
        active (BooleanField): Checkbox field for user's active status.
        submit (SubmitField): Button to submit the form.
    """

    username = StringField("Username", render_kw={"readonly": True})
    email = StringField("Email", render_kw={"readonly": True})
    role = SelectMultipleField(
        "User Role",
        choices=[
            ("Reader", "Reader"),
            ("Admin", "Admin"),
            ("Superadmin", "Superadmin"),
        ],
    )
    active = BooleanField("Active")
    submit = SubmitField("Change Role")


# Form for Adding New User
class CreateNewUserForm(FlaskForm):
    """
    A FlaskForm class for creating a new user.

    Attributes:
        name (StringField): Field to input the user's name.
        username (StringField): Field to input the username.
        email (StringField): Field to input the email.
        role (SelectMultipleField): Multi-select field for selecting user roles.
        active (BooleanField): Checkbox field for user's active status.
        submit (SubmitField): Button to submit the form.
    """

    name = StringField("Name")
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required."),
            Length(
                min=3,
                max=15,
                message="Username must be between 3 and 15 characters long. Please choose a different one!",
            ),
            validate_username,
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email is required."),
            Email(),
            validate_email,
        ],
    )
    role = SelectMultipleField(
        "User Role",
        choices=[
            ("Reader", "Reader"),
            ("Admin", "Admin"),
            ("Superadmin", "Superadmin"),
        ],
    )
    active = BooleanField("Active", default=True)
    submit = SubmitField("Add User")


# User Account Settings
class UserAccountSettingsForm(FlaskForm):
    """
    A FlaskForm class for editing user account settings.

    Attributes:
        name (StringField): Field to input the user's name.
        username (StringField): Field to input the username.
        email (StringField): Field to input the email.
        submitAccountSettings (SubmitField): Button to submit account settings changes.
    """

    name = StringField("Name")
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required. Please enter your username!"),
            Length(
                min=3,
                max=15,
                message="Username must be between 3 and 15 characters long. Please choose a different one!",
            ),
            validate_username_update,
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email is required. Please enter your email!"),
            Email(),
            validate_email_update,
        ],
    )
    submitAccountSettings = SubmitField("Save")


# Form for changing user password
class UserChangePasswordForm(FlaskForm):
    """
    A FlaskForm class for changing a user's password.

    Attributes:
        password (PasswordField): Field to input the new password.
        confirm_password (PasswordField): Field to confirm the new password.
        submitChangePassword (SubmitField): Button to submit password change.
    """

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required. Please enter your password!"),
            validate_password,
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Please retype your password!"),
            EqualTo("password", message="Passwords must match!"),
        ],
    )
    submitChangePassword = SubmitField("Change Password")
