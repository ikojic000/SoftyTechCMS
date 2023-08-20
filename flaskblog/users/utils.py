from datetime import datetime
from flask_login import current_user

from flaskblog.models import User


# Utility method that checks if a user has a specific role
def user_has_role(user, target_role):
    return any(role.name == target_role for role in user.roles)


# Method for getting user count for a single month
def get_users_count(month):
    current_year = datetime.utcnow().year
    start_date = datetime(current_year, month, 1)
    if month == 12:
        end_date = datetime(current_year + 1, 1, 1)
    else:
        end_date = datetime(current_year, month + 1, 1)

    user_count = User.query.filter(
        User.email_confirmed_at >= start_date, User.email_confirmed_at < end_date
    ).count()

    # response = {"month": month, "year": current_year, "user_count": user_count}
    # return jsonify(response)
    return user_count
