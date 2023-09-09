from flask import Blueprint, redirect, url_for, flash, render_template, request, session
from flask_login import current_user, login_user, logout_user
from passlib.hash import bcrypt
from SoftyTechCMS.auth.oauth_utils import facebook, google
from SoftyTechCMS.auth.forms import LoginForm, RegisterForm
from SoftyTechCMS.logs.request_logging import after_request, before_request
from SoftyTechCMS.users.database_manager import (
    create_or_get_user,
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


@auth.route("/login/google")
def google_login():
    """
    Initiate the Google OAuth2 login process.

    Returns:
        redirect: Redirects to the Google OAuth2 authorization page.
    """
    return google.authorize(callback=url_for("auth.google_authorized", _external=True))


@auth.route("/login/google/authorized")
def google_authorized():
    """
    Handle the Google OAuth2 authorization callback.

    Returns:
        redirect: Redirects the user to the home page after successful login.
    """
    # Retrieve the response from the Google OAuth2 authorization request
    response = google.authorized_response()
    if response is None or response.get("access_token") is None:
        # If the response is missing or does not contain an access token, show an error message
        flash(
            "Access denied: reason={} error={}".format(
                request.args["error_reason"], request.args["error_description"]
            ),
            "danger",
        )
        return redirect(url_for("main.home"))

    # Add the access token to the session
    session["google_token"] = (response["access_token"], "")

    # Fetch user information from Google using the access token
    user_info = google.get("userinfo")
    if "email" in user_info.data:
        email = user_info.data["email"]
        username = user_info.data["email"].split("@")[
            0
        ]  # Extract the username from the email
        name = user_info.data.get("name")  # Get the user's name if available, or None

        # Create or retrieve the user from database
        user = create_or_get_user(email, username, name)  # Pass the user data
        login_user(user)  # Log in the user
        flash("Logged in via Google!", "success")
        return redirect(url_for("main.home"))
    else:
        flash(
            "Unable to retrieve user data from Google.", "danger"
        )  # Show an error message
        return redirect(url_for("main.home"))


@auth.route("/login/facebook")
def facebook_login():
    """
    Initiate the Facebook OAuth2 login process.

    Returns:
        redirect: Redirects to the Facebook OAuth2 authorization page.
    """
    return facebook.authorize(
        callback=url_for("auth.facebook_authorized", _external=True)
    )


@auth.route("/login/facebook/authorized")
def facebook_authorized():
    """
    Handle the Facebook OAuth2 authorization callback.

    Returns:
        redirect: Redirects the user to the home page after successful login.
    """
    # Retrieve the response from the Facebook OAuth2 authorization request
    response = facebook.authorized_response()
    if response is None or response.get("access_token") is None:
        # If the response is missing or does not contain an access token, show an error message
        flash(
            "Access denied: reason={} error={}".format(
                request.args["error_reason"], request.args["error_description"]
            ),
            "danger",
        )
        return redirect(url_for("main.home"))

    # Add the access token to the session
    session["facebook_token"] = (response["access_token"], "")

    # Fetch user information from Facebook using the access token
    user_info = facebook.get("/me?fields=id,email,name")
    if "email" in user_info.data:
        email = user_info.data["email"]
        username = user_info.data["email"].split("@")[
            0
        ]  # Extract the username from the email
        name = user_info.data.get("name")  # Get the user's name

        # Create or retrieve the user from database
        user = create_or_get_user(email, username, name)  # Pass the user data
        login_user(user)  # Log in the user
        flash("Logged in via Facebook!", "success")
        return redirect(url_for("main.home"))
    else:
        flash(
            "Unable to retrieve user data from Facebook.", "danger"
        )  # Show an error message
        return redirect(url_for("main.home"))


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
