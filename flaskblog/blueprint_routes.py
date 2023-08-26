from flaskblog import app
from flaskblog.auth.routes import auth
from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.categories.routes import categories
from flaskblog.comments.routes import comments
from flaskblog.logs.routes import logs
from flaskblog.errors.routes import errors
from flaskblog.main.routes import main


def routes():
    """
    Register all the application's blueprints for different routes.

    This function registers the blueprints for various components of the application,
    including authentication, user management, posts, categories, comments, logs, errors, and main routes.

    Returns:
        None
    """
    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(categories)
    app.register_blueprint(comments)
    app.register_blueprint(logs)
    app.register_blueprint(errors)
    app.register_blueprint(main)
