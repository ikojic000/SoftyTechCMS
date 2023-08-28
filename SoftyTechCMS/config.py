from SoftyTechCMS import app
import os


filemanager_route = os.path.join(app.root_path, "static/upload")


class Config:
    SECRET_KEY = os.environ.get("SoftyTechCMS_SECRET_KEY")

    # Lenovo Yoga Database Config
    SQLALCHEMY_DATABASE_URI = os.environ.get("SoftyTechCMS_SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Mail setting
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("SoftyTechCMS_MAIL_USER")
    MAIL_PASSWORD = os.environ.get("SoftyTechCMS_MAIL_PASSWORD")
    USER_EMAIL_SENDER_EMAIL = os.environ.get("SoftyTechCMS_MAIL_USER")

    # Filemanager settings
    FLASKFILEMANAGER_FILE_PATH = filemanager_route

    # Flask-User settings
    USER_APP_NAME = "SoftyTech"
    USER_LOGIN_TEMPLATE = "/admin_Login.html"
    USER_FORGOT_PASSWORD_TEMPLATE = "/form-templates/resetPassword.html"
    USER_CHANGE_PASSWORD_TEMPLATE = "/form-templates/changePassword.html"
    USER_RESET_PASSWORD_TEMPLATE = "/form-templates/changeResetPassword.html"
    USER_LOGIN_URL = "/login"
    USER_CHANGE_PASSWORD_URL = "/user/change-password"
    USER_ENABLE_USERNAME = True
    USER_AUTO_LOGIN_AFTER_RESET_PASSWORD = False
