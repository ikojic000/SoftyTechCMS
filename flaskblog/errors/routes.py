# errors/routes.py
from flask import Blueprint, g, request, render_template, g, abort, url_for
from flask_login import current_user
from datetime import datetime
from flaskblog.models import ErrorLog
from flaskblog import db

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(400)
def not_found_error(error):
    return render_error_page(400, error)


@errors.app_errorhandler(401)
def forbidden_error(error):
    return render_error_page(401, error)


@errors.app_errorhandler(403)
def forbidden_error(error):
    return render_error_page(403, error)


@errors.app_errorhandler(404)
def not_found_error(error):
    return render_error_page(404, error)


@errors.app_errorhandler(500)
def internal_error(error):
    return render_error_page(500, error)


def render_error_page(status_code, error):
    user_id = current_user.id if current_user.is_authenticated else None

    error_log = ErrorLog(
        user_id=user_id,
        endpoint=request.endpoint,
        methodType=request.method,
        status_code=status_code,
        error_message=str(error),
    )

    db.session.add(error_log)
    db.session.commit()

    context = {"status_code": status_code, "error": error}

    return render_template("error.html", **context)
