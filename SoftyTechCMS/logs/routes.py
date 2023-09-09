import json

from flask import Blueprint, render_template
from flask import Response
from flask_login import login_required
from flask_user import roles_required

from SoftyTechCMS.logs.database_manager import (
	delete_logs,
	get_all_error_logs,
	get_all_request_logs,
)
from SoftyTechCMS.logs.request_logging import after_request, before_request
from SoftyTechCMS.logs.utils import generate_csv, prepare_logs_data
from SoftyTechCMS.models import RequestLog, ErrorLog

# Create a Blueprint for managing logs
logs = Blueprint("logs", __name__)

# Register before and after request handlers for logging
logs.before_request(before_request)
logs.after_request(after_request)


# Route to display all request logs (admin view)
@logs.route("/admin/logs/request", methods=[ "GET" ])
@login_required
@roles_required("Superadmin")
def request_logs( ):
	"""
	Display all request logs in a table.

	Returns:
		render_template: Renders the admin-request-logs.html template.
	"""
	title = "Request Logs"
	requestLogs = get_all_request_logs( )
	
	context = {
		"title": title,
		"pageTitle": title,
		"requestLogs": requestLogs,
	}
	
	return render_template("admin/admin-request-logs.html", **context)


# Route to display all error logs (admin view)
@logs.route("/admin/logs/error", methods=[ "GET" ])
@login_required
@roles_required("Superadmin")
def error_logs( ):
	"""
	Display all error logs in a table.

	Returns:
		render_template: Renders the admin-request-logs.html template.
	"""
	title = "Error Logs"
	errorLogs = get_all_error_logs( )
	
	context = {
		"title": title,
		"pageTitle": title,
		"errorLogs": errorLogs,
	}
	
	return render_template("admin/admin-request-logs.html", **context)


# Route to delete all request logs
@logs.route("/admin/logs/request/delete")
@login_required
@roles_required("Superadmin")
def delete_all_request_logs( ):
	"""
	Delete all request logs from the database.

	Returns:
		redirect: Redirects to the admin page after deleting logs.
	"""
	return delete_logs(RequestLog)


# Route to delete all error logs
@logs.route("/admin/logs/error/delete")
@login_required
@roles_required("Superadmin")
def delete_all_error_logs( ):
	"""
	Delete all error logs from the database.

	Returns:
		redirect: Redirects to the admin page after deleting logs.
	"""
	return delete_logs(ErrorLog)


# Route to download request logs in JSON format
@logs.route("/admin/logs/request/download/json", methods=[ "GET" ])
@login_required
@roles_required("Superadmin")
def download_request_logs_json( ):
	"""
	Download request logs in JSON format.

	Returns:
		Response: A JSON response containing the request logs data as a file download.
	"""
	data = prepare_logs_data(RequestLog)
	
	response = Response(
		json.dumps(data, indent=4),
		content_type="application/json",
		headers={ "Content-Disposition": "attachment;filename=request_logs.json" },
	)
	
	return response


# Route to download request logs in CSV format
@logs.route("/admin/logs/request/download/csv", methods=[ "GET" ])
@login_required
@roles_required("Superadmin")
def download_request_logs_csv( ):
	"""
	Download request logs in CSV format.

	Returns:
		Response: A CSV response containing the request logs data as a file download.
	"""
	data = prepare_logs_data(RequestLog)
	
	headers = [
		"ID",
		"Timestamp",
		"Endpoint",
		"Method",
		"User",
	]
	
	csv_data = [ headers ] + [ list(log.values( )) for log in data ]
	
	response = Response(
		generate_csv(csv_data),
		content_type="text/csv",
		headers={ "Content-Disposition": "attachment;filename=request_logs.csv" },
	)
	
	return response


# Route to download error logs in JSON format
@logs.route("/admin/logs/error/download/json", methods=[ "GET" ])
@login_required
@roles_required("Superadmin")
def download_error_logs_json( ):
	"""
	Download error logs in JSON format.

	Returns:
		Response: A JSON response containing the error logs data as a file download.
	"""
	data = prepare_logs_data(ErrorLog)
	
	response = Response(
		json.dumps(data, indent=4),
		content_type="application/json",
		headers={ "Content-Disposition": "attachment;filename=error_logs.json" },
	)
	
	return response


# Route to download error logs in CSV format
@logs.route("/admin/logs/error/download/csv", methods=[ "GET" ])
@login_required
@roles_required("Superadmin")
def download_error_logs_csv( ):
	"""
	Download error logs in CSV format.

	Returns:
		Response: A CSV response containing the error logs data as a file download.
	"""
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
	
	csv_data = [ headers ] + [ list(log.values( )) for log in data ]
	
	response = Response(
		generate_csv(csv_data),
		content_type="text/csv",
		headers={ "Content-Disposition": "attachment;filename=error_logs.csv" },
	)
	
	return response
