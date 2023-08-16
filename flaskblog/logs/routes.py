from flask import Blueprint, render_template
from flask_login import login_required
from flask_user import roles_required
from flaskblog import db

from flaskblog.models import RequestLog, User, ErrorLog

logs = Blueprint("logs", __name__)


@logs.route("/admin/logs/request", methods=["GET"])
@login_required
@roles_required("Superadmin")
def request_logs():
    title = "Request Logs"

    requestLogs = RequestLog.query.all()

    return render_template(
        "admin/admin-request-logs.html",
        title=title,
        pageTitle=title,
        requestLogs=requestLogs,
    )


@logs.route("/admin/logs/error", methods=["GET"])
@login_required
@roles_required("Superadmin")
def error_logs():
    title = "Error Logs"
    errorLogs = ErrorLog.query.all()
    print("TEST - ERROR LOGS")

    return render_template(
        "admin/admin-test.html",
        title=title,
        pageTitle=title,
        errorLogs=errorLogs,
    )
