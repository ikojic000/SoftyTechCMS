from flask_login import current_user


# Utility method that checks if a user has a specific role
def user_has_role(user, target_role):
    return any(role.name == target_role for role in user.roles)


# Utility method for FileManager access
def accessControl_function():
    if current_user.is_authenticated:
        if user_has_role(current_user, "Admin") or user_has_role(
            current_user, "Superuser"
        ):
            return True
        else:
            return False
    else:
        return False
