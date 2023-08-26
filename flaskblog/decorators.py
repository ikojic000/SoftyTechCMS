from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def own_account_required(view_func):
    """
    Decorator that checks if the current user owns the requested account.

    This decorator is used to restrict access to views where users can update their own account settings,
    ensuring that only the user who owns the account can access and modify their settings.

    Args:
        view_func: The view function being decorated.

    Returns:
        function: A decorated view function.
    """

    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        # Get the user_id from the route parameters
        user_id = kwargs.get("user_id")

        # Check if the current user is authenticated and owns the requested account
        if current_user.is_authenticated and current_user.id == user_id:
            return view_func(*args, **kwargs)
        else:
            # If not authenticated or authorized, flash a message and redirect to the login page
            flash("You must be logged in and authorized to access this page.")
            return redirect(
                url_for("auth.login")
            )  # You can change 'login' to your login route

    return decorated_view
