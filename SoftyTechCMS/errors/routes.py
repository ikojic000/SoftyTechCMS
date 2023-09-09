from flask import Blueprint, request, render_template
from flask_login import current_user

from SoftyTechCMS.errors.database_manager import save_error_log

# Create a Blueprint for error handling named 'errors'
errors = Blueprint("errors", __name__)


# Define error handlers for different HTTP error codes
@errors.app_errorhandler(400)
def not_found_error( error ):
	"""
	Handle a 400 Bad Request error.

	Args:
		error: The error object.

	Returns:
		A rendered error page.
	"""
	return render_error_page(400, error)


@errors.app_errorhandler(401)
def forbidden_error( error ):
	"""
	Handle a 401 Unauthorized error.

	Args:
		error: The error object.

	Returns:
		A rendered error page.
	"""
	return render_error_page(401, error)


@errors.app_errorhandler(403)
def forbidden_error( error ):
	"""
	Handle a 403 Forbidden error.

	Args:
		error: The error object.

	Returns:
		A rendered error page.
	"""
	return render_error_page(403, error)


@errors.app_errorhandler(404)
def not_found_error( error ):
	"""
	Handle a 404 Not Found error.

	Args:
		error: The error object.

	Returns:
		A rendered error page.
	"""
	return render_error_page(404, error)


@errors.app_errorhandler(500)
def internal_error( error ):
	"""
	Handle a 500 Internal Server Error.

	Args:
		error: The error object.

	Returns:
		A rendered error page.
	"""
	return render_error_page(500, error)


# Define a function to render error pages
def render_error_page( status_code, error ):
	"""
	Render an error page with the given status code and error message.

	Args:
		status_code (int): The HTTP status code.
		error: The error object.

	Returns:
		A rendered error page.
	"""
	# Determine the user's ID if they are authenticated, otherwise set it to None
	user_id = current_user.id if current_user.is_authenticated else None
	
	# Save error log information to the database
	save_error_log(user_id, request.endpoint, request.method, status_code, error)
	
	# Create a context dictionary with status code and error message
	context = { "status_code": status_code, "error": error }
	
	# Render the 'error.html' template with the context data
	return render_template("error.html", **context)
