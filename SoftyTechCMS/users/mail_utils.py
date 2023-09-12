from flask_mail import Message

from SoftyTechCMS import mail, db
from SoftyTechCMS.models import ErrorLog


def send_register_mail(user):
	"""
	Send a registration confirmation email to the user.

	Args:
		user: The user object to whom the email will be sent.

	Raises:
		Exception: If there is an issue with sending the email.

	This function sends a welcome email to the user upon registration.
	"""
	subject = "Welcome to SoftyTech"
	message_body = f"Dear {user.email},\n\nThank you for registering to SoftyTech.\n\nPlease enjoy your time here.\n\nSincerely,\nSoftyTech"
	
	message = Message(subject=subject, recipients=[user.email])
	message.body = message_body
	
	try:
		mail.send(message)
	except Exception as e:
		error = ErrorLog(error_message=str(e))
		# Add the error log object to the database session
		db.session.add(error)
		# Commit the database session to save the error log
		db.session.commit()


def send_oauth_register_mail(user):
	"""
	Send a registration confirmation email to the user who registered using OAuth.

	Args:
		user: The user object to whom the email will be sent.

	Raises:
		Exception: If there is an issue with sending the email.

	This function sends a welcome email to the user who registered using Google or Facebook OAuth.
	"""
	subject = "Welcome to SoftyTech"
	message_body = f"Dear {user.email},\n\nThank you for registering to SoftyTech.\n\nAs you logged in with your Google/Facebook account please change your generated password.\n\nYour credentials:\nEmail: {user.email}\nPassword: SoftyTech123\n\nAfter that, you can log in with your Google/Facebook account or with your SoftyTech account.\n\nPlease enjoy your time here.\n\nSincerely,\nSoftyTech"
	
	message = Message(subject=subject, recipients=[user.email])
	message.body = message_body
	
	try:
		mail.send(message)
	except Exception as e:
		error = ErrorLog(error_message=str(e))
		# Add the error log object to the database session
		db.session.add(error)
		# Commit the database session to save the error log
		db.session.commit()
