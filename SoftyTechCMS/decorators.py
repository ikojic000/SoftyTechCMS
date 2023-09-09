from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

from SoftyTechCMS.comments.database_manager import get_comment_by_id


def own_account_required( view_func ):
	"""
	Decorator that checks if the current user owns the requested account.

	This decorator is used to restrict access to views where users can update their own account settings,
	ensuring that only the user who owns the account can access and modify their settings.

	Args:
		view_func: The view function being decorated.

	Returns:
		function: A decorated view function.
	"""
	
	
	@wraps(view_func)
	def decorated_view( *args, **kwargs ):
		# Get the user_id from the route parameters
		user_id = kwargs.get("user_id")
		
		# Check if the current user is authenticated and owns the requested account
		if current_user.is_authenticated and current_user.id == user_id:
			return view_func(*args, **kwargs)
		else:
			# If not authenticated or authorized, flash a message and redirect to the login page
			flash("You must be logged in and authorized to access this page.")
			return redirect(
				url_for("auth.login")
			)  # You can change 'login' to your login route
	
	
	return decorated_view


def owner_of_comment_required( view_func ):
	"""
	Decorator that checks if the current user owns the requested comment.

	This decorator is used to restrict access to views where users can delete their own comments,
	ensuring that only the user who owns the comment can delete it.

	Args:
		view_func: The view function being decorated.

	Returns:
		function: A decorated view function.
	"""
	
	
	@wraps(view_func)
	def decorated_view( comment_id, *args, **kwargs ):
		# Get the comment object using the provided comment_id
		comment = get_comment_by_id(comment_id)
		
		# Check if the current user is authenticated and owns the requested comment
		if current_user.is_authenticated and comment.user_id == current_user.id:
			return view_func(comment_id, *args, **kwargs)
		else:
			# If not authenticated or authorized, flash a message and redirect
			flash("You must be logged in and authorized to delete this comment.")
			return redirect(url_for("your_login_route"))  # Change to your login route
	
	
	return decorated_view
