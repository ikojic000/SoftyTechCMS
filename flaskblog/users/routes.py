
from flask import render_template, url_for, redirect, flash, request, make_response, Blueprint
from flaskblog import app, db, bcrypt
from flaskblog.users.forms import LoginForm, RegisterForm, UpdateAccountForm, UpdateAccountRoleForm
from flaskblog.models import User, Post, UserRoles
from flask_login import login_user, logout_user, current_user, login_required
from flask_user import roles_required
import os



users = Blueprint('users', __name__)


# Route for User Account 
# Displaying user account details and updating account function
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', form=form, title=current_user.username)


@users.route("/account/<int:user_id>/delete", methods=['GET'])
@login_required
def delete_account(user_id):
    print(user_id)
    logout_user()
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash('You have deleted your account..', 'success')
    return redirect(url_for('main.home'))



# Admin HomePage
@users.route("/admin")
@login_required
@roles_required('Admin')
def admin():
    users = User.query.all()
    posts = Post.query.all()
    return render_template('admin_home.html', users=users, posts=posts)


# Registering to a website
# Admin and User side Route
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.automaticRole', user_id = user.id))
    return render_template('register.html', title='Register', form=form)

# Automatically giving role 'reader' when registered
@users.route("/register/<int:user_id>/role", methods=['GET', 'POST'])
def automaticRole(user_id):
    user = User.query.filter_by(id=user_id).first()
    user_role = UserRoles(user_id=user_id, role_id='1')
    db.session.add(user_role)
    db.session.commit()
    return redirect(url_for('users.login'))


# Logging into a website
# Admin and User side Route
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print("login12345")
            login_user(user)
            next_page = request.args.get('next')
            flash('Logged In!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Failed! Please check your email and password', 'danger')
    return render_template('admin_Login.html', title='Login', form=form)


# Logging out User
# Admin and User side Route
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))


# Displaying users in a table
@users.route("/admin/users")
@login_required
@roles_required('Admin')
def userList():
    users = User.query.all()
    return render_template('admin_Users.html', users=users)


# Deleting User from the database
@users.route("/user/<int:user_id>/delete", methods=['GET'])
@login_required
@roles_required('Admin')
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted!', 'success')
    return redirect(url_for('users.userList'))


# Updating User in the database
@users.route("/user/<int:user_id>/update", methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    user_role = UserRoles.query.filter_by(user_id=user.id).first()
    form = UpdateAccountRoleForm()
    if form.validate_on_submit():
        user_role.role_id = form.role.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.userList'))
    elif request.method == 'GET':
        form.role.data = user_role.role_id
    return render_template('userAccountUpdate.html', form=form, user=user)