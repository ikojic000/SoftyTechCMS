from flask import flash, abort, redirect, url_for

from SoftyTechCMS import db
from SoftyTechCMS.models import ErrorLog, RequestLog


def get_all_request_logs( ):
	"""
	Get all request logs from the database.

	Returns:
		list of RequestLog: List of RequestLog objects.
	"""
	return RequestLog.query.all( )


def get_all_error_logs( ):
	"""
	Get all error logs from the database.

	Returns:
		list of ErrorLog: List of ErrorLog objects.
	"""
	return ErrorLog.query.all( )


def delete_logs( log_model ):
	"""
	Delete logs from the database.

	Args:
		log_model (class): The model class representing the type of logs to be deleted.

	Returns:
		redirect: Redirects to the admin page after deleting logs.
	"""
	try:
		# Delete logs using the provided model class
		num_deleted = log_model.query.delete( )
		
		if num_deleted > 0:
			# If logs were deleted, commit the changes to the database
			db.session.commit( )
			flash(f"Deleted {num_deleted} logs.", "success")
		else:
			# If no logs were deleted, display an info message
			flash("No logs to delete.", "info")
	
	except Exception as e:
		# Handle any exceptions that occur during deletion
		flash("An error occurred while deleting logs.", "error")
		db.session.rollback( )
		abort(500, "An error occurred while deleting logs. Please try again.")
	
	return redirect(url_for("users.admin"))


def save_request_log( endpoint, method, user_id, timestamp ):
	"""
	Save a request log entry to the database.

	Args:
		endpoint (str): The endpoint where the request occurred.
		method (str): The HTTP method type (e.g., GET, POST) used for the request.
		user_id (int): The ID of the user associated with the request (if applicable).
		timestamp (datetime): The timestamp of the request.

	Returns:
		None
	"""
	try:
		# Create a new RequestLog object and add it to the database
		request_log = RequestLog(
			endpoint=endpoint, methodType=method, user_id=user_id, timestamp=timestamp
		)
		
		db.session.add(request_log)
		db.session.commit( )
	except Exception as e:
		db.session.rollback( )
