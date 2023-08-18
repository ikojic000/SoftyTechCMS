from flask import (
    render_template,
    url_for,
    redirect,
    flash,
    request,
    make_response,
    Blueprint,
    jsonify,
)

from flaskblog import app, db
from passlib.hash import bcrypt
from flaskblog.users.forms import (
    LoginForm,
    RegisterForm,
    UpdateAccountForm,
    UpdateAccountRoleForm,
    UserRoleForm,
)
from flaskblog.models import User, Post, UserRoles, Role, Comment
from flask_login import login_user, logout_user, current_user, login_required
from flask_user import roles_required
from sqlalchemy import or_
from datetime import datetime
from flaskblog.users.utils import user_has_role


users = Blueprint("users", __name__)

# Method for getting adding user_has_role function to jinja templates
app.jinja_env.globals.update(user_has_role=user_has_role)


# Route for User Account
# Displaying user account details and updating account function
@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", form=form, title=current_user.username)


@users.route("/account/<int:user_id>/delete", methods=["GET"])
@login_required
def delete_account(user_id):
    print(user_id)
    logout_user()
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash("You have deleted your account..", "success")
    return redirect(url_for("main.home"))


# Admin HomePage - Dashboard - New
@users.route("/admin")
@login_required
@roles_required(["Admin", "Superadmin"])
def admin():
    pageTitle = "Dashboard"
    return render_template(
        "admin/admin-dashboard.html",
        pageTitle=pageTitle,
    )


# Registering to a website
# Admin and User side Route
@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegisterForm()
    if form.validate_on_submit():
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
        #     "utf-8"
        # )
        hashed_password = bcrypt.hash(form.password.data)
        role_reader = Role.query.filter_by(name="Reader").first_or_404()
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        user.roles.append(role_reader)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


# Logging into a website
# Admin and User side Route
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(
            or_(User.email == form.email.data, User.username == form.email.data)
        ).first()
        if user and bcrypt.verify(form.password.data, user.password):
            print("login12345")
            login_user(user)
            next_page = request.args.get("next")
            flash("Logged In!", "success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Failed! Please check your email and password", "danger")
    return render_template("admin_Login.html", title="Login", form=form)


# Logging out User
# Admin and User side Route
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))


# Dashoard - Table wih all users with edit/delete buttons - New
@users.route("/admin/users/all")
@login_required
@roles_required(["Admin", "Superadmin"])
def all_users():
    users = User.query.all()
    title = "All Users"
    return render_template(
        "admin/admin-users.html", users=users, title=title, pageTitle=title
    )


# Showing Details, Posts, and Comments by User - New
@users.route("/admin/user/preview/<int:user_id>")
@login_required
@roles_required(["Admin", "Superadmin"])
def user_details(user_id):
    title = "User Details"
    user = User.query.filter_by(id=user_id).first_or_404()
    posts = Post.query.filter_by(author=user.username).all()
    comments = (
        Comment.query.join(User, Comment.user_id == User.id)
        .join(Post, Comment.post_id == Post.id)
        .filter(Comment.user_id == user_id)
        .all()
    )

    return render_template(
        "admin/admin-preview-user.html",
        title=title,
        pageTitle=title,
        user=user,
        posts=posts,
        comments=comments,
    )


# Deleting User from the database - New
@users.route("/admin/users/delete/<int:user_id>", methods=["GET", "POST"])
@login_required
@roles_required(["Admin", "Superadmin"])
def delete_user(user_id):
    title = "Delete User"
    user = User.query.filter_by(id=user_id).first_or_404()
    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        flash("User has been deleted!", "success")
        return redirect(url_for("users.all_users"))

    return render_template(
        "admin/admin-delete-user.html", title=title, pageTitle=title, user=user
    )


# Updating User in the database - New
@users.route("/admin/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
@roles_required(["Admin", "Superadmin"])
def change_user_role(user_id):
    title = "Change User settings"
    user = User.query.get_or_404(user_id)

    form = UserRoleForm(
        username=user.username,
        email=user.email,
        role=[
            role.name for role in user.roles
        ],  # Pass the selected roles / roles that user has
        active=user.active,
    )

    is_user_superadmin = user_has_role(user, "Superadmin")

    if form.validate_on_submit():
        new_role_names = form.role.data
        if not user_has_role(current_user, "Superadmin"):
            if is_user_superadmin:
                new_role_names.append("Superadmin")
        updated_roles = [
            Role.query.filter_by(name=role_name).first() for role_name in new_role_names
        ]
        user.roles = updated_roles

        user.active = form.active.data
        db.session.commit()

        source = request.args.get("source", "all_users")
        return redirect(
            url_for(
                "users.all_users" if source == "all_users" else "users.user_details",
                user_id=user.id,
            )
        )

    return render_template(
        "admin/admin-change-user-settings.html",
        form=form,
        user=user,
        pageTitle=title,
        title=title,
    )


# # Updating User in the database - New
# @users.route("/admin/edit/<int:user_id>", methods=["GET", "POST"])
# @login_required
# @roles_required(["Admin", "Superadmin"])
# def change_user_role(user_id):
#     title = "Change User settings"
#     user = User.query.get_or_404(user_id)

#     selected_roles = [role.name for role in user.roles]  # Get the user's roles
#     form = UserRoleForm(
#         username=user.username,
#         email=user.email,
#         role=selected_roles,  # Pass the selected roles
#         active=user.active,
#     )

#     is_user_superadmin = user_has_role(user, "Superadmin")

#     if form.validate_on_submit():
#         # Update user's roles based on form submission

#         if user_has_role(current_user, "Superadmin"):
#             new_role_names = form.role.data

#             # Clear existing roles and assign the new roles
#             user.roles.clear()
#             for role_name in new_role_names:
#                 role = Role.query.filter_by(name=role_name).first()
#                 if role:
#                     user.roles.append(role)
#         else:
#             new_role_names = form.role.data
#             if is_user_superadmin:
#                 new_role_names.append("Superadmin")
#             user.roles.clear()
#             for role_name in new_role_names:
#                 role = Role.query.filter_by(name=role_name).first()
#                 if role:
#                     user.roles.append(role)

#         user.active = form.active.data
#         db.session.commit()

#         source = request.args.get("source")
#         if source == "all_users":
#             return redirect(url_for("users.all_users"))
#         elif source == "user_details":
#             return redirect(url_for("users.user_details", user_id=user.id))
#         else:
#             return redirect(url_for("users.all_users"))

#     return render_template(
#         "admin/admin-change-user-settings.html", form=form, user=user, pageTitle=title
#     )


# Updating User in the database
@users.route("/user/<int:user_id>/update", methods=["GET", "POST"])
@login_required
@roles_required(["Admin", "Superadmin"])
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    user_role = UserRoles.query.filter_by(user_id=user.id).first()
    form = UpdateAccountRoleForm()
    if form.validate_on_submit():
        user_role.role_id = form.role.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.userList"))
    elif request.method == "GET":
        form.role.data = user_role.role_id
    return render_template("userAccountUpdate.html", form=form, user=user)


@users.route("/user/number_of_users", methods=["GET"])
def number_of_users():
    number_of_users = User.query.count()
    return jsonify(number_of_users=number_of_users)


# Method for user count for all months
@users.route("/api/users/count_by_months", methods=["GET"])
def posts_count():
    usersCountList = []

    for x in range(1, 13):
        usersCountList.append(get_users_count(x))

    return jsonify(usersCountList=usersCountList)


# Util methods


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
