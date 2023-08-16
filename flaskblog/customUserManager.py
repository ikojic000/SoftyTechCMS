from flask_user import UserManager
from flask import abort, request, flash, redirect


class CustomUserManager(UserManager):
    def unauthorized_view(self):
        """Prepare a Flash message and redirect to USER_UNAUTHORIZED_ENDPOINT"""
        # Prepare Flash message
        url = request.script_root + request.path
        message = "TEST - You do not have permission to access " + url + ". - TEST"
        flash(message, "error")

        # Redirect to USER_UNAUTHORIZED_ENDPOINT
        # return redirect(self._endpoint_url(self.USER_UNAUTHORIZED_ENDPOINT))
        abort(401)
