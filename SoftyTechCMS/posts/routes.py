import os

from flask import (
	render_template,
	url_for,
	redirect,
	flash,
	request,
	Blueprint,
	make_response,
)
from flask.json import jsonify
from flask_login import current_user, login_required
from flask_user import roles_required

from SoftyTechCMS import app
from SoftyTechCMS.logs.request_logging import after_request, before_request
from SoftyTechCMS.posts.database_manager import (
	count_posts,
	create_post,
	delete_all_users_posts,
	get_all_posts,
	get_post_by_id,
	post_delete,
	post_update,
	publish_unpublish_post,
)
from SoftyTechCMS.posts.forms import PostForm
from SoftyTechCMS.posts.utils import gen_rnd_filename, get_posts_count, save_head_image

# Create a Blueprint for the 'posts' module
posts = Blueprint("posts", __name__)

# Register before and after request functions for logging
posts.before_request(before_request)
posts.after_request(after_request)


# Route for displaying all posts for admin users
@posts.route("/admin/posts/all")
@login_required
@roles_required(["Admin", "Superadmin"])
def all_posts():
	"""
	Display all posts in an admin interface with edit and delete buttons.

	Returns:
		HTML: Rendered template displaying all posts.
	"""
	# Get all posts from the database
	posts = get_all_posts()
	title = "All Posts"
	
	# Create a context dictionary for rendering the template
	context = {
		"posts": posts,
		"pageTitle": title,
		"title": title,
	}
	return render_template("admin/admin-posts.html", **context)


# Route for adding a new post to the database
@posts.route("/admin/posts/new", methods=["GET", "POST"])
@login_required
@roles_required(["Admin", "Superadmin"])
def add_post():
	"""
	Add a new post to the database.

	Returns:
		HTML: Rendered template for creating a new post.
	"""
	title = "Add New Post"
	form = PostForm(author=current_user.username)
	
	# Check if the form has been submitted and is valid
	if form.validate_on_submit():
		# Initialize headImg to None
		headImg = None
		if form.headImg.data:
			# Save the uploaded head image and set headImg to its filename
			headImg = save_head_image(form.headImg.data, form.title.data)
		
		# Create a new post in the database
		create_post(
			form.title.data,
			form.subtitle.data,
			form.description.data,
			headImg,
			form.slug.data,
			form.language.data,
			form.author.data,
			form.content.data,
			form.isPublished.data,
			form.category.data,
		)
		
		# Display a success message and redirect to the 'all_posts' route
		flash("Post Added", "success")
		return redirect(url_for("posts.all_posts"))
	
	# Create a context dictionary for rendering the template
	context = {"pageTitle": title, "form": form, "title": title}
	
	return render_template("admin/admin-post-create.html", **context)


# Route for updating an existing post
@posts.route("/admin/posts/update/<int:post_id>", methods=["GET", "POST"])
@login_required
@roles_required(["Admin", "Superadmin"])
def update_post(post_id):
	"""
	Update an existing post in the database.

	Args:
		post_id (int): The ID of the post to be updated.

	Returns:
		HTML: Rendered template for updating a post.
	"""
	title = "Update Post"
	post = get_post_by_id(post_id)
	form = PostForm(obj=post)
	current_headImg = post.headImg
	
	# Check if the form has been submitted and is valid
	if form.validate_on_submit():
		# Check if a new image file has been provided
		if form.headImg.data:
			# Save the uploaded head image and update post's headImg attribute
			headImg = save_head_image(form.headImg.data, form.title.data)
			post.headImg = headImg
			headImgData = headImg
		else:
			post.headImg = current_headImg
			headImgData = current_headImg
		
		# Update post in the database
		post_update(
			post,
			form.title.data,
			form.subtitle.data,
			form.description.data,
			form.slug.data,
			form.language.data,
			form.author.data,
			form.content.data,
			form.isPublished.data,
			form.category.data,
			headImgData,
		)
		
		source = request.args.get("source")
		if source == "all_posts":
			return redirect(url_for("posts.all_posts"))
		elif source == "user_details":
			user_id = request.args.get("user_id")
			if user_id is not None:
				return redirect(url_for("users.user_details", user_id=user_id))
		else:
			return redirect(url_for("posts.all_posts"))
	
	# Set the form's category field with the ID of the category associated with the post
	form.category.data = post.category
	# Construct the URL for the image
	if post.headImg:
		image_url = url_for(
			"static",
			filename=f"upload/media/images/head_Images/{post.headImg}",
		)
	else:
		image_url = None
	
	print("Image URL: " + image_url)
	# Set the form's headImg data to the image URL
	form.headImg.data = image_url
	
	context = {
		"pageTitle": title,
		"title": title,
		"form": form,
	}
	return render_template("admin/admin-post-create.html", **context)


# Route for changing a post's isPublished attribute to True or False
@posts.route("/admin/posts/publish/<int:post_id>", methods=["GET", "POST"])
@login_required
@roles_required(["Admin", "Superadmin"])
def publish_post(post_id):
	"""
	Change a post's isPublished attribute to True or False.

	Args:
		post_id (int): The ID of the post to be published/unpublished.

	Returns:
		HTTP Redirect: Redirects to the appropriate page based on the 'source' query parameter.
	"""
	# Call the 'publish_unpublish_post' function to toggle the post's isPublished attribute
	publish_unpublish_post(post_id)
	
	# Get the 'source' query parameter from the request URL
	source = request.args.get("source")
	
	# Redirect to the appropriate page based on the 'source' parameter
	if source == "all_posts":
		return redirect(url_for("posts.all_posts"))
	elif source == "user_details":
		user_id = request.args.get("user_id")
		if user_id is not None:
			return redirect(url_for("users.user_details", user_id=user_id))
	else:
		return redirect(url_for("posts.all_posts"))


# Route for deleting a post
@posts.route("/admin/posts/delete/<int:post_id>", methods=["GET", "POST"])
@login_required
@roles_required(["Admin", "Superadmin"])
def delete_post(post_id):
	"""
	Delete a post from the database.

	Args:
		post_id (int): The ID of the post to be deleted.

	Returns:
		HTML or HTTP Redirect: Depending on the HTTP request method, either renders the deletion confirmation page
		or redirects to the appropriate page based on the 'source' query parameter after deletion.
	"""
	title = "Delete Post"
	post = get_post_by_id(post_id)
	
	# Check if the request method is POST (indicating a confirmation to delete)
	if request.method == "POST":
		# Call the 'post_delete' function to delete the post from the database
		post_delete(post)
		
		# Display a success message
		flash("Post Deleted", "success")
		
		# Get the 'source' query parameter from the request URL
		source = request.args.get("source")
		
		# Redirect to the appropriate page based on the 'source' parameter
		if source == "all_posts":
			return redirect(url_for("posts.all_posts"))
		elif source == "user_details":
			user_id = request.args.get("user_id")
			if user_id is not None:
				return redirect(url_for("users.user_details", user_id=user_id))
		else:
			return redirect(url_for("posts.all_posts"))
	
	# If the request method is GET, render the deletion confirmation page
	context = {
		"pageTitle": title,
		"title": title,
		"post": post,
	}
	return render_template("admin/admin-post-delete.html", **context)


# Method for deleting all posts by a specific user
@posts.route("/admin/posts/delete/user/<int:user_id>")
@login_required
@roles_required(["Admin", "Superadmin"])
def delete_all_posts_by_user(user_id):
	"""
	Delete all posts by a specific user from the database.

	Args:
		user_id (int): The ID of the user whose posts are to be deleted.

	Returns:
		HTTP Redirect: Redirects to the user's details page after deleting the user's posts.
	"""
	# Call the 'delete_all_users_posts' function to delete all posts by the specified user
	delete_all_users_posts(user_id)
	
	# Redirect to the user's details page
	return redirect(url_for("users.user_details", user_id=user_id))


# Method that returns the total number of posts
@posts.route("/post/number_of_posts", methods=["GET"])
def number_of_posts():
	"""
	Return the total number of posts in the database.

	Returns:
		JSON: JSON response containing the number of posts.
	"""
	# Call the 'count_posts' function to get the total number of posts
	number_of_posts = count_posts()
	
	return jsonify(number_of_posts=number_of_posts)


# Method that returns the total number of posts by each month
@posts.route("/api/posts/count_by_months", methods=["GET"])
def posts_count():
	"""
	Return the total number of posts for each month of the year.

	Returns:
		JSON: JSON response containing a list of post counts for each month.
	"""
	postsCountList = []
	
	# Iterate through months (1 to 12) and get the post count for each month
	for x in range(1, 13):
		postsCountList.append(get_posts_count(x))
	
	return jsonify(postsCountList=postsCountList)


@posts.route("/ckupload/", methods=["POST", "OPTIONS", "GET"])
def ckupload():
	"""
	CKEditor file upload endpoint.

	Handles file uploads for CKEditor and returns the URL of the uploaded file.

	Returns:
		HTTP Response: Returns a response containing JavaScript to communicate with CKEditor.
	"""
	error = ""
	url = ""
	callback = request.args.get("CKEditorFuncNum")
	
	# Check if the request method is POST and contains the 'upload' file
	if request.method == "POST" and "upload" in request.files:
		fileobj = request.files["upload"]
		
		# Get the filename and file extension
		fname, fext = os.path.splitext(fileobj.filename)
		rnd_name = "%s%s" % (gen_rnd_filename(), fext)
		
		# Define the file path where the uploaded file will be saved
		filepath = os.path.join(app.root_path, "static/upload/media/images", rnd_name)
		dirname = os.path.dirname(filepath)
		
		# Check if the directory for file storage exists; create if not
		if not os.path.exists(dirname):
			try:
				os.makedirs(dirname)
			except:
				error = "ERROR_CREATE_DIR"
		# Check if the directory is writeable
		elif not os.access(dirname, os.W_OK):
			error = "ERROR_DIR_NOT_WRITEABLE"
		
		# If no errors occurred, save the file to the specified path
		if not error:
			fileobj.save(filepath)
			url = url_for(
				"static", filename="%s/%s" % ("upload/media/images/", rnd_name)
			)
			print(url)
	else:
		error = "post error"
		res = """<script type="text/javascript">
             window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
             </script>""" % (
			callback,
			url,
			error,
		)
	
	# Create an HTTP response containing JavaScript to communicate with CKEditor
	response = make_response(res)
	response.headers["Content-Type"] = "text/html"
	return response
