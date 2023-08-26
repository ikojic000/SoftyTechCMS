from flask_user import UserManager
from flask import abort, request, flash, redirect


class CustomUserManager(UserManager):
    """
    Custom user manager class that extends the UserManager class provided by Flask-User.
    """

    def unauthorized_view(self):
        """
        Handle unauthorized access.

        This method prepares a Flash message and redirects to the USER_UNAUTHORIZED_ENDPOINT.

        Returns:
            None
        """
        # Prepare Flash message
        url = request.script_root + request.path
        message = "You do not have permission to access " + url + "."
        flash(message, "error")

        # Abort the request with a 401 Unauthorized status code
        abort(401)
