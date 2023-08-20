from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, logout_user
from passlib.hash import bcrypt
from sqlalchemy import or_
from flaskblog import db
from flaskblog.auth.forms import LoginForm, RegisterForm
from flaskblog.logs.request_logging import after_request, before_request
from flaskblog.models import Role, User


auth = Blueprint("auth", __name__)

auth.before_request(before_request)
auth.after_request(after_request)


# Registering to a website
# Admin and User side Route
@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegisterForm()
    if form.validate_on_submit():
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
        #     "utf-8"
        # )
        hashed_password = bcrypt.hash(form.password.data)
        print("Hashed password: ", hashed_password)
        role_reader = Role.query.filter_by(name="Reader").first_or_404()
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        user.roles.append(role_reader)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", title="Register", form=form)


# Logging into a website
# Admin and User side Route
@auth.route("/login", methods=["GET", "POST"])
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
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
