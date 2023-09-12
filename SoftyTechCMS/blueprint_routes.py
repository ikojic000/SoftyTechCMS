from SoftyTechCMS import app
from SoftyTechCMS.auth.routes import auth
from SoftyTechCMS.categories.routes import categories
from SoftyTechCMS.comments.routes import comments
from SoftyTechCMS.errors.routes import errors
from SoftyTechCMS.logs.routes import logs
from SoftyTechCMS.main.routes import main
from SoftyTechCMS.posts.routes import posts


def routes():
	"""
	Register all the application's blueprints for different routes.

	This function registers the blueprints for various components of the application,
	including authentication, user management, posts, categories, comments, logs, errors, and main routes.

	Returns:
		None
	"""
	app.register_blueprint(auth)
	app.register_blueprint(posts)
	app.register_blueprint(categories)
	app.register_blueprint(comments)
	app.register_blueprint(logs)
	app.register_blueprint(errors)
	app.register_blueprint(main)
