import csv
import io
from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import login_required
from flask_user import roles_required
from flaskblog import db
import json
from flask import Response
from flaskblog.models import RequestLog, User, ErrorLog

logs = Blueprint("logs", __name__)


@logs.route("/admin/logs/request", methods=["GET"])
@login_required
@roles_required("Superadmin")
def request_logs():
    title = "Request Logs"
    requestLogs = RequestLog.query.all()

    context = {
        "title": title,
        "pageTitle": title,
        "requestLogs": requestLogs,
    }

    return render_template("admin/admin-request-logs.html", **context)


@logs.route("/admin/logs/error", methods=["GET"])
@login_required
@roles_required("Superadmin")
def error_logs():
    title = "Error Logs"
    errorLogs = ErrorLog.query.all()

    context = {
        "title": title,
        "pageTitle": title,
        "errorLogs": errorLogs,
    }

    return render_template("admin/admin-request-logs.html", **context)


@logs.route("/admin/logs/request/delete")
@login_required
@roles_required("Superadmin")
def delete_all_request_logs():
    return delete_logs(RequestLog)


@logs.route("/admin/logs/error/delete")
@login_required
@roles_required("Superadmin")
def delete_all_error_logs():
    return delete_logs(ErrorLog)


def delete_logs(log_model):
    try:
        num_deleted = log_model.query.delete()

        if num_deleted > 0:
            db.session.commit()
            flash(f"Deleted {num_deleted} logs.", "success")
        else:
            flash("No logs to delete.", "info")

    except Exception as e:
        flash("An error occurred while deleting logs.", "error")
        db.session.rollback()
        abort(500)

    return redirect(url_for("users.admin"))


def prepare_logs_data(log_model):
    logs_data = log_model.query.all()
    data = []

    for log in logs_data:
        log_data = {
            "id": log.id,
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "user": log.user.username,
        }

        if isinstance(log, RequestLog):
            log_data.update(
                {
                    "endpoint": log.endpoint,
                    "method": log.methodType,
                }
            )
        elif isinstance(log, ErrorLog):
            log_data.update(
                {
                    "endpoint": log.endpoint,
                    "method": log.methodType,
                    "status_code": log.status_code,
                    "error_message": log.error_message,
                }
            )

        data.append(log_data)

    return data


def generate_csv(data):
    output = io.StringIO()
    csv_writer = csv.writer(output)

    for row in data:
        csv_writer.writerow(row.values())

    return output.getvalue()


@logs.route("/admin/logs/request/download/json", methods=["GET"])
@login_required
@roles_required("Superadmin")
def download_request_logs_json():
    data = prepare_logs_data(RequestLog)

    response = Response(
        json.dumps(data, indent=4),
        content_type="application/json",
        headers={"Content-Disposition": "attachment;filename=request_logs.json"},
    )

    return response


@logs.route("/admin/logs/request/download/csv", methods=["GET"])
@login_required
@roles_required("Superadmin")
def download_request_logs_csv():
    data = prepare_logs_data(RequestLog)

    headers = [
        "ID",
        "Timestamp",
        "Endpoint",
        "Method",
        "User",
    ]

    csv_data = [headers] + [list(log.values()) for log in data]

    response = Response(
        generate_csv(csv_data),
        content_type="text/csv",
        headers={"Content-Disposition": "attachment;filename=request_logs.csv"},
    )

    return response


@logs.route("/admin/logs/error/download/json", methods=["GET"])
@login_required
@roles_required("Superadmin")
def download_error_logs_json():
    data = prepare_logs_data(ErrorLog)

    response = Response(
        json.dumps(data, indent=4),
        content_type="application/json",
        headers={"Content-Disposition": "attachment;filename=error_logs.json"},
    )

    return response


@logs.route("/admin/logs/error/download/csv", methods=["GET"])
@login_required
@roles_required("Superadmin")
def download_error_logs_csv():
    data = prepare_logs_data(ErrorLog)

    headers = [
        "ID",
        "Timestamp",
        "Endpoint",
        "Method",
        "Status Code",
        "Error Message",
        "User",
    ]

    csv_data = [headers] + [list(log.values()) for log in data]

    response = Response(
        generate_csv(csv_data),
        content_type="text/csv",
        headers={"Content-Disposition": "attachment;filename=error_logs.csv"},
    )

    return response
