from flaskblog import app
import os


filemanager_route = os.path.join(app.root_path, "static/upload")


class Config:
    SECRET_KEY = "y.o.u.s.h.a.l.l.n.o.t.k.n.o.w"
    # Lenovo Legion Database Config
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:administrator@localhost/softy_empty?charset=utf8mb4'

    # Lenovo Yoga Database Config
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:root@localhost/softy_empty?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Mail setting
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    # MAIL_USERNAME = os.environ.get('MAIL_USER')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USERNAME = "softythetechguy@gmail.com"  # set os enviroment variable
    MAIL_PASSWORD = "nfcvarzskksghcpk"  # set os enviroment variable
    USER_EMAIL_SENDER_EMAIL = "softythetechguy@gmail.com"

    # Filemanager settings
    FLASKFILEMANAGER_FILE_PATH = filemanager_route

    # Flask-User settings
    USER_APP_NAME = "SoftyTech"
    USER_LOGIN_TEMPLATE = "/admin_Login.html"
    USER_FORGOT_PASSWORD_TEMPLATE = "/form-templates/resetPassword.html"
    USER_CHANGE_PASSWORD_TEMPLATE = "/form-templates//changePassword.html"
    USER_RESET_PASSWORD_TEMPLATE = "/form-templates/changeResetPassword.html"
    USER_LOGIN_URL = "/login"
    USER_CHANGE_PASSWORD_URL = "/user/change-password"
    USER_ENABLE_USERNAME = True
    USER_AUTO_LOGIN_AFTER_RESET_PASSWORD = False
