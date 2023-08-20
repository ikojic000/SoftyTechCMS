from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def own_account_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        user_id = kwargs.get("user_id")
        if current_user.is_authenticated and current_user.id == user_id:
            return view_func(*args, **kwargs)
        else:
            flash("You must be logged in and authorized to access this page.")
            return redirect(
                url_for("auth.login")
            )  # You can change 'login' to your login route

    return decorated_view
