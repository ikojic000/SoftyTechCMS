from SoftyTechCMS.users.database_manager import users_count_in_single_month


# Utility method that checks if a user has a specific role
def user_has_role( user, target_role ):
	"""
	Check if a user has a specific role.

	Args:
		user: The user object to check.
		target_role (str): The role to check for.

	Returns:
		bool: True if the user has the target role, False otherwise.
	"""
	return any(role.name == target_role for role in user.roles)


# Method for getting user count for a single month
def get_users_count( month ):
	"""
	Get the count of users for a single month.

	Args:
		month (int): The month for which to get the user count.

	Returns:
		int: The count of users for the specified month.
	"""
	user_count = users_count_in_single_month(month)
	return user_count
