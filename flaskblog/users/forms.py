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
from flask_wtf.file import FileAllowed
from flaskblog.auth.utils import (
    validate_email,
    validate_email_update,
    validate_password,
    validate_username,
    validate_username_update,
)
from flaskblog.models import User, Role
from flask_login import current_user


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


# Form foe Addin New User
class CreateNewUserForm(FlaskForm):
    name = StringField("Name")
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=15), validate_username],
    )
    email = StringField("Email", validators=[DataRequired(), Email(), validate_email])
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
        validators=[DataRequired(), Length(min=3, max=15), validate_username_update],
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), validate_email_update]
    )
    submitAccountSettings = SubmitField("Save")


class UserChangePasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), validate_password])
    confirm_password = PasswordField(
        "Confirm Password", validators=[EqualTo("password")]
    )
    submitChangePassword = SubmitField("Change Password")
