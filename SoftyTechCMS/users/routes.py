from flask import (
    render_template,
    url_for,
    redirect,
    flash,
    request,
    Blueprint,
    jsonify,
)
from flask_login import current_user, login_required
from flask_user import roles_required

from SoftyTechCMS import app, user_email_manager
from SoftyTechCMS.comments.database_manager import get_comments_by_user_id
from SoftyTechCMS.decorators import own_account_required
from SoftyTechCMS.logs.request_logging import after_request, before_request
from SoftyTechCMS.posts.database_manager import get_posts_by_author
from SoftyTechCMS.users.database_manager import (
    count_users,
    create_new_user,
    get_all_users,
    get_user_by_id,
    update_user_account,
    update_user_password,
    update_user_role_and_active,
    user_delete,
)
from SoftyTechCMS.users.forms import (
    CreateNewUserForm,
    UserAccountSettingsForm,
    UserChangePasswordForm,
    UserRoleForm,
)
from SoftyTechCMS.users.utils import get_users_count, user_has_role

# Create a Blueprint for user-related routes
users = Blueprint("users", __name__)

# Apply 'before_request' and 'after_request' middleware functions to the 'users' Blueprint
users.before_request(before_request)
users.after_request(after_request)

# Add 'user_has_role' function to the Jinja templates, making it available for rendering
app.jinja_env.globals.update(user_has_role=user_has_role)


# Define a route for the admin homepage/dashboard
@users.route("/admin")
@login_required
@roles_required([ "Admin", "Superadmin" ])
def admin( ):
	"""
	Render the admin homepage/dashboard.

	Requires authentication and roles 'Admin' or 'Superadmin' to access.

	Returns:
		HTTP Response: Renders the admin dashboard template.
	"""
	pageTitle = "Dashboard"
	return render_template(
		"admin/admin-dashboard.html",
		pageTitle=pageTitle,
	)


# Route for displaying a table of all users with edit/delete buttons
@users.route("/admin/users/all")
@login_required
@roles_required([ "Admin", "Superadmin" ])
def all_users( ):
	"""
	Render a table of all users with edit/delete buttons in the admin panel.

	Requires authentication and roles 'Admin' or 'Superadmin' to access.

	Returns:
		HTTP Response: Renders the admin users template.
	"""
	users = get_all_users( )
	title = "All Users"
	return render_template(
		"admin/admin-users.html", users=users, title=title, pageTitle=title
	)


# Route for displaying user details, posts, and comments
@users.route("/admin/user/preview/<int:user_id>")
@login_required
@roles_required([ "Admin", "Superadmin" ])
def user_details( user_id ):
	"""
	Render user details, posts, and comments for a specific user in the admin panel.

	Requires authentication and roles 'Admin' or 'Superadmin' to access.

	Args:
		user_id (int): The ID of the user to display details for.

	Returns:
		HTTP Response: Renders the user details template.
	"""
	title = "User Details"
	user = get_user_by_id(user_id)
	posts = get_posts_by_author(user.username)
	comments = get_comments_by_user_id(user.id)
	
	return render_template(
		"admin/admin-user-preview.html",
		title=title,
		pageTitle=title,
		user=user,
		posts=posts,
		comments=comments,
	)


# Route for creating a new user and adding them to the database
@users.route("/admin/users/new", methods=[ "GET", "POST" ])
@login_required
@roles_required([ "Admin", "Superadmin" ])
def create_user( ):
	"""
	Render a form to create a new user and add them to the database in the admin panel.

	Requires authentication and roles 'Admin' or 'Superadmin' to access.

	Returns:
		HTTP Response: Renders the user creation form template.
	"""
	title = "Create User"
	form = CreateNewUserForm( )
	
	if form.validate_on_submit( ):
		create_new_user(
			form.username.data,
			form.email.data,
			form.name.data,
			form.active.data,
			form.role.data,
		)
		
		flash("User created successfully", "success")
		return redirect(url_for("users.all_users"))
	
	context = { "form": form, "title": title, "pageTitle": title }
	return render_template("admin/admin-user-create.html", **context)


# Route for deleting a user from the database
@users.route("/admin/users/delete/<int:user_id>", methods=[ "GET", "POST" ])
@login_required
@roles_required([ "Admin", "Superadmin" ])
def delete_user( user_id ):
	"""
	Render a confirmation page for deleting a user from the database in the admin panel.

	Requires authentication and roles 'Admin' or 'Superadmin' to access.

	Args:
		user_id (int): The ID of the user to be deleted.

	Returns:
		HTTP Response: Renders the user deletion confirmation template.
	"""
	title = "Delete User"
	user = get_user_by_id(user_id)
	
	if request.method == "POST":
		user_delete(user)
		flash("User has been deleted!", "success")
		return redirect(url_for("users.all_users"))
	
	return render_template(
		"admin/admin-user-delete.html", title=title, pageTitle=title, user=user
	)


# Route for updating user settings in the database
@users.route("/admin/edit/<int:user_id>", methods=[ "GET", "POST" ])
@login_required
@roles_required([ "Admin", "Superadmin" ])
def change_user_role( user_id ):
	"""
	Render a form to change user settings and update them in the database in the admin panel.

	Requires authentication and roles 'Admin' or 'Superadmin' to access.

	Args:
		user_id (int): The ID of the user whose settings are being updated.

	Returns:
		HTTP Response: Renders the user settings form template.
	"""
	# Define the title for the page
	title = "Change User settings"
	
	# Get the user by their ID from the database
	user = get_user_by_id(user_id)
	
	# Create a form for changing user settings with pre-filled data
	form = UserRoleForm(
		username=user.username,
		email=user.email,
		role=[
			role.name for role in user.roles
		],  # Pass the selected roles / roles that user has
		active=user.active,
	)
	
	# Check if the user being edited is a 'Superadmin'
	is_user_superadmin = user_has_role(user, "Superadmin")
	
	if form.validate_on_submit( ):
		# Get the new role names and consider 'Superadmin' role restrictions
		new_role_names = form.role.data
		if not user_has_role(current_user, "Superadmin"):
			if is_user_superadmin:
				new_role_names.append("Superadmin")
		
		# Update the user's roles and active status in the database
		update_user_role_and_active(user, new_role_names, form.active.data)
		
		# Determine the source URL based on the request arguments
		source = request.args.get("source", "all_users")
		
		# Redirect to the appropriate URL after updating user settings
		return redirect(
			url_for(
				"users.all_users" if source == "all_users" else "users.user_details",
				user_id=user.id,
			)
		)
	
	# Render the user settings form template with the form and user data
	return render_template(
		"admin/admin-user-access-settings.html",
		form=form,
		user=user,
		pageTitle=title,
		title=title,
	)


# Route for updating user account settings
@users.route("/user/account-settings/<int:user_id>", methods=[ "GET", "POST" ])
@login_required
@own_account_required
def update_user_account_settings( user_id ):
	"""
	Render a form to update user account settings and change password in the user panel.

	Requires authentication, and the user must own the account.

	Args:
		user_id (int): The ID of the user whose account settings are being updated.

	Returns:
		HTTP Response: Renders the user account settings form template.
	"""
	# Define the title for the page
	title = "Update User Settings"
	
	# Get the user by their ID from the database
	user = get_user_by_id(user_id)
	
	# Create forms for updating user settings and changing the password
	userSettingsForm = UserAccountSettingsForm(obj=user)
	changePasswordForm = UserChangePasswordForm( )
	
	# Handle form submission for updating user account settings
	if userSettingsForm.submitAccountSettings.data and userSettingsForm.validate( ):
		update_user_account(
			user,
			userSettingsForm.name.data,
			userSettingsForm.username.data,
			userSettingsForm.email.data,
		)
		user_email_manager.send_username_changed_email(current_user)
		flash("User settings updated successfully", "success")
		return redirect(url_for("users.update_user_account_settings", user_id=user.id))
	
	# Handle form submission for changing the user's password
	if changePasswordForm.submitChangePassword.data and changePasswordForm.validate( ):
		update_user_password(user, changePasswordForm.password.data)
		user_email_manager.send_password_changed_email(current_user)
		flash("Password updated successfully", "success")
		return redirect(url_for("users.update_user_account_settings", user_id=user.id))
	
	context = {
		"user": user,
		"userSettingsForm": userSettingsForm,
		"changePasswordForm": changePasswordForm,
		"pageTitle": title,
		"title": title,
	}
	
	# Check if the current user has 'Admin' or 'Superadmin' roles and render the appropriate template
	if user_has_role(current_user, "Admin") or user_has_role(
			current_user, "Superadmin"
	):
		return render_template("admin/admin-user-settings.html", **context)
	
	# Render the user account settings form template for regular users
	return render_template("form-templates/user-settings.html", **context)


# Route for getting the number of users
@users.route("/user/number_of_users", methods=[ "GET" ])
def number_of_users( ):
	"""
	Get the number of users and return it as JSON.

	Returns:
		JSON Response: Contains the number of users.
	"""
	number_of_users = count_users( )
	return jsonify(number_of_users=number_of_users)


# Route for getting the user count for all months
@users.route("/api/users/count_by_months", methods=[ "GET" ])
def posts_count( ):
	"""
	Get the user count for all months and return it as JSON.

	Returns:
		JSON Response: Contains a list of user counts for each month.
	"""
	usersCountList = [ ]
	
	# Loop through months and retrieve user counts for each month
	for x in range(1, 13):
		usersCountList.append(get_users_count(x))
	
	return jsonify(usersCountList=usersCountList)
