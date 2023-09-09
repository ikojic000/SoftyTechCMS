from datetime import datetime

from flask import flash, abort
from passlib.hash import bcrypt
from sqlalchemy import or_

from SoftyTechCMS import db
from SoftyTechCMS.models import Role, User
from SoftyTechCMS.users.mail_utils import send_register_mail, send_oauth_register_mail


# Get a user by their username
def get_user_by_username( username ):
	"""
	Retrieve a user by their username.

	Args:
		username (str): The username of the user to retrieve.

	Returns:
		User or None: The User object if found, or None if not found.
	"""
	return User.query.filter_by(username=username).first( )


# Get a user by their email
def get_user_by_email( email ):
	"""
	Retrieve a user by their email.

	Args:
		email (str): The email address of the user to retrieve.

	Returns:
		User or None: The User object if found, or None if not found.
	"""
	return User.query.filter_by(email=email).first( )


# Get a user by either their email or username
def get_user_by_username_email( input ):
	"""
	Retrieve a user by their email or username.

	Args:
		input (str): The email or username of the user to retrieve.

	Returns:
		User or None: The User object if found, or None if not found.
	"""
	return User.query.filter(or_(User.email == input, User.username == input)).first( )


# Get a user by their ID or return a 404 error if not found
def get_user_by_id( user_id ):
	"""
	Retrieve a user by their ID or raise a 404 error if not found.

	Args:
		user_id (int): The ID of the user to retrieve.

	Returns:
		User: The User object.

	Raises:
		404 Error: If the user is not found.
	"""
	return User.query.filter_by(id=user_id).first_or_404( )


# Get a list of all users
def get_all_users( ):
	"""
	Retrieve a list of all users.

	Returns:
		List[User]: A list of User objects representing all users.
	"""
	return User.query.all( )


# Get a role by its name
def get_role_by_name( role_name ):
	"""
	Retrieve a role by its name.

	Args:
		role_name (str): The name of the role to retrieve.

	Returns:
		Role or None: The Role object if found, or None if not found.
	"""
	return Role.query.filter_by(name=role_name).first( )


# Create a new user and assign roles
def create_new_user( username, email, name, active, roles ):
	"""
	Create a new user with the provided information and assign roles to the user.

	Args:
		username (str): The username for the new user.
		email (str): The email address for the new user.
		name (str): The name of the new user.
		active (bool): The user's active status (True or False).
		roles (list): A list of role names to assign to the user.

	Returns:
		None
	"""
	try:
		# Hash the default password
		hashed_password = bcrypt.hash("SoftyTest123")
		
		# Create a new User object with the provided information
		user = User(
			username=username,
			email=email,
			password=hashed_password,
			name=name,
			active=active,
		)
		
		# Assign roles to the user
		for role in roles:
			user_role = get_role_by_name(role)
			if user_role:
				user.roles.append(user_role)
		
		# Add the user to the database and commit the changes
		db.session.add(user)
		db.session.commit( )
	except Exception as e:
		flash("An error occurred while creating the user.", "error")
		db.session.rollback( )
		abort(
			500,
			"An error occurred while saving the user to the database. Please try again later.",
		)


# Register a new user with the provided information and assign a 'Reader' role
def register_user( name, username, email, password ):
	"""
	Register a new user with the provided information and assign a 'Reader' role to the user.

	Args:
		name (str): The name of the new user.
		username (str): The username for the new user.
		email (str): The email address for the new user.
		password (str): The password for the new user (plain text).

	Returns:
		None
	"""
	try:
		# Hash the provided password for security
		hashed_password = bcrypt.hash(password)
		
		# Get the 'Reader' role from the database
		role_reader = get_role_by_name("Reader")
		
		# Create a new User object with the provided information
		user = User(name=name, username=username, email=email, password=hashed_password)
		
		# Assign the 'Reader' role to the user
		user.roles.append(role_reader)
		
		# Add the user to the database and commit the changes
		db.session.add(user)
		db.session.commit( )
		# Sending welcome mail to newly registered user
		send_register_mail(user)
	except Exception as e:
		flash("An error occurred while registering the user.", "error")
		db.session.rollback( )
		abort(
			500,
			"An error occurred while saving the user to the database. Please try again later.",
		)


# Delete a user from the database
def user_delete( user ):
	"""
	Delete a user from the database.

	Args:
		user (User): The user object to be deleted.

	Returns:
		None
	"""
	try:
		# Delete the user from the database
		db.session.delete(user)
		db.session.commit( )
	except Exception as e:
		flash("An error occurred while deleting the user.", "error")
		db.session.rollback( )
		abort(500, "An error occurred while deleting the user. Please try again later.")


# Update a user's roles and active status in the database
def update_user_role_and_active( user, new_role_names, is_active ):
	"""
	Update a user's roles and active status in the database.

	Args:
		user (User): The user object to be updated.
		new_role_names (list): A list of role names to assign to the user.
		is_active (bool): The new active status for the user.

	Returns:
		None
	"""
	try:
		# Get the updated roles based on the provided role names
		updated_roles = [ get_role_by_name(role_name) for role_name in new_role_names ]
		
		# Update the user's roles and active status
		user.roles = updated_roles
		user.active = is_active
		
		# Commit the changes to the database
		db.session.commit( )
	except Exception as e:
		flash(
			"An error occurred while updating the user's roles and active status.",
			"error",
		)
		db.session.rollback( )
		abort(
			500,
			"An error occurred while updating the user's roles and active status. Please try again later.",
		)


# Update a user's account information in the database
def update_user_account( user, name, username, email ):
	"""
	Update a user's account information in the database.

	Args:
		user (User): The user object to be updated.
		name (str): The new name for the user.
		username (str): The new username for the user.
		email (str): The new email address for the user.

	Returns:
		None
	"""
	try:
		# Update the user's account information
		user.name = name
		user.username = username
		user.email = email
		
		# Commit the changes to the database
		db.session.commit( )
	except Exception as e:
		flash(
			"An error occurred while updating the user's account information.", "error"
		)
		db.session.rollback( )
		abort(
			500,
			"An error occurred while updating the user's account information. Please try again later.",
		)


# Update a user's password in the database
def update_user_password( user, new_password ):
	"""
	Update a user's password in the database.

	Args:
		user (User): The user object whose password will be updated.
		new_password (str): The new password for the user (plain text).

	Returns:
		None
	"""
	try:
		# Hash the new password for security
		hashed_password = bcrypt.hash(new_password)
		
		# Update the user's password
		user.password = hashed_password
		
		# Commit the changes to the database
		db.session.commit( )
	except Exception as e:
		flash("An error occurred while updating the user's password.", "error")
		db.session.rollback( )
		abort(
			500,
			"An error occurred while updating the user's password. Please try again later.",
		)


# Method for OAuth2 authentication - finding the user by email or creating a new one
def create_or_get_user( email, username, name=None ):
	"""
	Create a new user or retrieve an existing user with the provided email.

	Args:
		email (str): The email address of the user.
		username (str): The username of the user.
		name (str, optional): The name of the user. Defaults to None.

	Returns:
		User: The User object representing the created or retrieved user.
	"""
	try:
		# Check if a user with the provided email already exists in the database
		existing_user = User.query.filter_by(email=email).first( )
		
		if existing_user:
			return existing_user
		else:
			# Create a new user with the provided email, username, and name
			new_user = User(
				email=email,
				username=username,
				name=name,
				password=bcrypt.hash("SoftyTech123"),
			)
			# Get the 'Reader' role from the database
			role_reader = get_role_by_name("Reader")
			# Assign the 'Reader' role to the user
			new_user.roles.append(role_reader)
			db.session.add(new_user)
			db.session.commit( )
			# Sending welcome mail to newly registered user
			send_oauth_register_mail(new_user)
			return new_user
	except Exception as e:
		flash("An error occurred while creating or retrieving the user.", "error")
		db.session.rollback( )


# Get the total number of users in the database
def count_users( ):
	"""
	Get the total number of users in the database.

	Returns:
		int: The total number of users.
	"""
	return User.query.count( )


# Get the number of users registered in a single month
def users_count_in_single_month( month ):
	"""
	Get the number of users registered in a specific month.

	Args:
		month (int): The month for which to retrieve the user count.

	Returns:
		int: The number of users registered in the specified month.
	"""
	current_year = datetime.utcnow( ).year
	start_date = datetime(current_year, month, 1)
	
	# Determine the end date based on the provided month
	if month == 12:
		end_date = datetime(current_year + 1, 1, 1)
	else:
		end_date = datetime(current_year, month + 1, 1)
	
	# Query the database to count users registered within the specified date range
	return User.query.filter(
		User.email_confirmed_at >= start_date, User.email_confirmed_at < end_date
	).count( )
