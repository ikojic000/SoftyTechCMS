# MAIN PYTHON FILE IN A flaskblog PACKAGE

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import flaskfilemanager


# App Configuration
app = Flask(__name__)  # Create a Flask application instance
db = SQLAlchemy(app)  # Initialize a SQLAlchemy database instance
mail = Mail()  # Create a Mail instance for sending emails
mail.init_app(app)  # Initialize the Mail instance with the Flask app


# Import configuration settings from Config class
from flaskblog.config import Config

app.config.from_object(Config)

# Initialize the LoginManager for user authentication
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"  # Set the login view route

# Import User and Post models
from flaskblog.models import User, Post

# Import custom user manager and access control function
from flaskblog.auth.customUserManager import CustomUserManager
from flaskblog.auth.utils import accessControl_function

# Initialize Flask-Filemanager with access control function
flaskfilemanager.init(app, access_control_function=accessControl_function)

filemanager_route = os.path.join(app.root_path, "static/upload")

# Import and register route blueprints using the routes function
from flaskblog.blueprint_routes import routes

# Registering blueprints using the routes function
routes()

# Initialize the CustomUserManager for user management
user_manager = CustomUserManager(app, db, User)
