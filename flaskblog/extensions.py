from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import flask_whooshalchemy as wa
import flaskfilemanager
from flaskblog.models import Post, User
from flaskblog.auth.utils import accessControl_function
from flaskblog.auth.customUserManager import CustomUserManager

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
flaskfilemanager = flaskfilemanager.Filer()


def initialize_extensions(app):
    db.init_app(app)

    mail.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    wa.whoosh_index(app, Post)  # Make sure to import 'Post' from your models

    flaskfilemanager.init(app, access_control_function=accessControl_function)

    user_manager = CustomUserManager(app, db, User)
    # You might have more extensions to initialize here
