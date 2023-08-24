# MAIN PYTHON FILE IN A flaskblog PACKAGE

# Imports

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_mail import Mail
import flask_whooshalchemy as wa
import flaskfilemanager


# App Configuration
app = Flask(__name__)
db = SQLAlchemy(app)
mail = Mail()
mail.init_app(app)

from flaskblog.config import Config

app.config.from_object(Config)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

from flaskblog.models import User, Post

# from flask_user import UserManager
from flaskblog.auth.customUserManager import CustomUserManager
from flaskblog.auth.utils import accessControl_function

flaskfilemanager.init(app, access_control_function=accessControl_function)

wa.whoosh_index(app, Post)

from flaskblog.blueprint_routes import routes

routes()

user_manager = CustomUserManager(app, db, User)
