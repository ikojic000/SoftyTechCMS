from SoftyTechCMS import db
from SoftyTechCMS.models import ErrorLog


# Define a function to save an error log entry to the database
def save_error_log( user_id, endpoint, methodType, status_code, error ):
	"""
	Save an error log entry to the database.

	Args:
		user_id (int): The ID of the user associated with the error (if applicable).
		endpoint (str): The endpoint where the error occurred.
		methodType (str): The HTTP method type (e.g., GET, POST) used for the request.
		status_code (int): The HTTP status code returned for the request.
		error (Exception): The error or exception that occurred.

	Returns:
		None
	"""
	try:
		# Create an ErrorLog object with the provided information
		error_log = ErrorLog(
			user_id=user_id,
			endpoint=endpoint,
			methodType=methodType,
			status_code=status_code,
			error_message=str(error),  # Convert the error to a string for storage
		)
		
		# Add the error log object to the database session
		db.session.add(error_log)
		
		# Commit the database session to save the error log
		db.session.commit( )
	except Exception as e:
		# In case of an exception, rollback the database session
		db.session.rollback( )
