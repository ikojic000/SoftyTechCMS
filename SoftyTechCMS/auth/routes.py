from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, logout_user
from passlib.hash import bcrypt
from SoftyTechCMS.auth.forms import LoginForm, RegisterForm
from SoftyTechCMS.logs.request_logging import after_request, before_request
from SoftyTechCMS.users.database_manager import (
    get_user_by_username_email,
    register_user,
)

# Create a Blueprint for authentication
auth = Blueprint("auth", __name__)

# Register before and after request handlers for logging
auth.before_request(before_request)
auth.after_request(after_request)


# Registering to a website - Admin and User side Route
@auth.route("/register", methods=["GET", "POST"])
def register():
    """
    Allow users to register for the website.

    Returns:
        redirect or render_template: Redirects to the login page after successful registration,
        or renders the registration form.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    # Create a RegisterForm instance
    form = RegisterForm()

    # Check if the form is submitted and valid
    if form.validate_on_submit():
        # Call the register_user function to create a new user
        register_user(
            form.name.data, form.username.data, form.email.data, form.password.data
        )
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("auth.login"))

    # Render the registration form
    return render_template("/form-templates/register.html", title="Register", form=form)


# Logging into a website - Admin and User side Route
@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Allow users to log in to the website.

    Returns:
        redirect or render_template: Redirects to the next page after successful login,
        or renders the login form.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    # Create a LoginForm instance
    form = LoginForm()

    # Check if the form is submitted and valid
    if form.validate_on_submit():
        # Get the user by username or email
        user = get_user_by_username_email(form.email.data)

        # Check if the user exists and the password is correct
        if user and bcrypt.verify(form.password.data, user.password):
            # Log in the user
            login_user(user)
            next_page = request.args.get("next")
            flash("Logged In!", "success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Failed! Please check your email and password", "danger")

    # Render the login form
    return render_template("/form-templates/login.html", title="Login", form=form)


# Logging out User - Admin and User side Route
@auth.route("/logout")
def logout():
    """
    Allow users to log out of the website.

    Returns:
        redirect: Redirects to the login page after logout.
    """
    logout_user()
    return redirect(url_for("auth.login"))
