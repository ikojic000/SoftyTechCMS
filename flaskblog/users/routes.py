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
from flaskblog.decorators import own_account_required
from flaskblog.users.forms import (
    CreateNewUserForm,
    UpdateAccountForm,
    UpdateAccountRoleForm,
    UserAccountSettingsForm,
    UserChangePasswordForm,
    UserRoleForm,
)
from flaskblog.models import User, Post, UserRoles, Role, Comment
from flask_login import current_user, login_required, logout_user
from flask_user import roles_required
from sqlalchemy import or_
from datetime import datetime
from flaskblog.users.utils import get_users_count, user_has_role


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
        "admin/admin-user-preview.html",
        title=title,
        pageTitle=title,
        user=user,
        posts=posts,
        comments=comments,
    )


# Adding new user to the database - New
@users.route("/admin/users/new", methods=["GET", "POST"])
@login_required
@roles_required(["Admin", "Superadmin"])
def create_user():
    title = "Create User"
    form = CreateNewUserForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.hash("SoftyTest123")

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            name=form.name.data,
            active=form.active.data,
        )

        for role in form.role.data:
            user_role = Role.query.filter_by(name=role).first()
            if user_role:
                user.roles.append(user_role)

        db.session.add(user)
        db.session.commit()

        flash("User created successfully", "success")
        return redirect(url_for("users.all_users"))

    context = {"form": form, "title": title, "pageTitle": title}
    return render_template("admin/admin-user-create.html", **context)


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
        "admin/admin-user-delete.html", title=title, pageTitle=title, user=user
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
        "admin/admin-user-access-settings.html",
        form=form,
        user=user,
        pageTitle=title,
        title=title,
    )


@users.route("/user/account-settings/<int:user_id>", methods=["GET", "POST"])
@login_required
@own_account_required
def update_user_account_settings(user_id):
    title = "Update User Settings"
    user = User.query.filter_by(id=user_id).first_or_404()

    # Bind the form to the User object
    userSettingsForm = UserAccountSettingsForm(obj=user)
    changePasswordForm = UserChangePasswordForm()

    # Handle form submission
    if userSettingsForm.submitAccountSettings.data and userSettingsForm.validate():
        user.name = userSettingsForm.name.data
        user.username = userSettingsForm.username.data
        user.email = userSettingsForm.email.data

        db.session.commit()
        flash("User settings updated successfully", "success")
        return redirect(url_for("users.update_user_account_settings", user_id=user.id))

    if changePasswordForm.submitChangePassword.data and changePasswordForm.validate():
        hashed_password = bcrypt.hash(changePasswordForm.password.data)
        user.password = hashed_password
        db.session.commit()
        flash("Password updated successfully", "success")
        return redirect(url_for("users.update_user_account_settings", user_id=user.id))

    context = {
        "user": user,
        "userSettingsForm": userSettingsForm,
        "changePasswordForm": changePasswordForm,
        "pageTitle": title,
        "title": title,
    }
    return render_template("admin/admin-user-settings.html", **context)


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


# Admin settings - updating your name, mail, username, password


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
