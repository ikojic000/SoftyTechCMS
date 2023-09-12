# MAIN PYTHON FILE IN A flaskblog PACKAGE

import os

import flaskfilemanager
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy

# App Configuration
app = Flask(__name__)  # Create a Flask application instance
db = SQLAlchemy(app)  # Initialize a SQLAlchemy database instance
mail = Mail()  # Create a Mail instance for sending emails
mail.init_app(app)  # Initialize the Mail instance with the Flask app
oauth = OAuth(app)  # Initialize the OAuth instance with the Flask app

# Import configuration settings from Config class
from SoftyTechCMS.config import Config

app.config.from_object(Config)

# Initialize the LoginManager for user authentication
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

# Import User and Post models
from SoftyTechCMS.models import User, Post

# Import custom user manager and access control function
from SoftyTechCMS.auth.customUserManager import CustomUserManager
from SoftyTechCMS.auth.utils import access_control_function

# Initialize Flask-Filemanager with access control function
flaskfilemanager.init(app, access_control_function=access_control_function)

filemanager_route = os.path.join(app.root_path, "static/upload")

# Import and register route blueprints using the routes function
from SoftyTechCMS.blueprint_routes import routes

# Registering blueprints using the routes function
routes()

# Initialize the CustomUserManager for user management
user_manager = CustomUserManager(app, db, User)

# Initialize Flask-User EmailManager for sending changed username/password mail notifications
from flask_user import EmailManager

user_email_manager = EmailManager(app)

from SoftyTechCMS.users.routes import users

app.register_blueprint(users)
