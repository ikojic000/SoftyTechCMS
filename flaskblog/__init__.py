# MAIN PYTHON FILE IN A flaskblog PACKAGE

# Imports

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
import flaskfilemanager

# App Configuration
app = Flask(__name__)
db = SQLAlchemy(app)
mail = Mail()
mail.init_app(app)
bcrypt = Bcrypt(app)


app.config.from_object(Config)


login_manager = LoginManager(app)
login_manager.login_view = 'login'


from flaskblog.models import User
from flask_user import UserManager
user_manager = UserManager(app, db, User)


print('000')
flaskfilemanager.init(app)

# Routes are last to be imported
from flaskblog import routes
from flaskblog import adminRoutes





