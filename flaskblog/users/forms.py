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
from flaskblog.auth.utils import (
    validate_email,
    validate_email_update,
    validate_password,
    validate_username,
    validate_username_update,
)
from flaskblog.models import Role


# FORMS
# USER SIDE FORMS


# Form for updating user account
class UpdateAccountForm(FlaskForm):
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


# Form for Roles - Admin
class UpdateAccountRoleForm(FlaskForm):
    role = StringField("Role", validators=[DataRequired()])
    submit = SubmitField("Update")


# Form for Changing user settings - Role & Active - New
class UserRoleForm(FlaskForm):
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


class UserChangePasswordForm(FlaskForm):
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
