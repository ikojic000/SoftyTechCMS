# MAIN PYTHON FILE IN A flaskblog PACKAGE

# Imports

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail

import flaskfilemanager

# App Configuration
app = Flask(__name__)
db = SQLAlchemy(app)
mail = Mail()
mail.init_app(app)
bcrypt = Bcrypt(app)

from flaskblog.config import Config
app.config.from_object(Config)


login_manager = LoginManager(app)
login_manager.login_view = 'users.login'


from flaskblog.models import User
from flask_user import UserManager
user_manager = UserManager(app, db, User)

def accessControl_function():
    if current_user.is_authenticated:
        if current_user.roles[0].name == 'Admin':
            return True
        else:
            return False
    else:
        return False

print('000')
flaskfilemanager.init(app, access_control_function = accessControl_function)

# Routes are last to be imported
 
from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)





