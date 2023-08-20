from flask import (
    render_template,
    url_for,
    redirect,
    flash,
    request,
    Blueprint,
    abort,
    make_response,
)
from flask.json import jsonify
from flaskblog import app, db
from flaskblog.logs.request_logging import after_request, before_request
from flaskblog.models import Category, Post, User
from flaskblog.posts.forms import PostForm
from flask_login import current_user, login_required
from flask_user import roles_required
from datetime import datetime
import os
import random

from flaskblog.posts.utils import get_posts_count, save_head_image


posts = Blueprint("posts", __name__)

posts.before_request(before_request)
posts.after_request(after_request)


# Dashoard - Table wih all posts with edit/delete buttons - New Design
@posts.route("/admin/posts/all")
@login_required
@roles_required(["Admin", "Superadmin"])
def all_posts():
    posts = Post.query.all()
    title = "All Posts"

    context = {
        "posts": posts,
        "pageTitle": title,
        "title": title,
    }
    return render_template("admin/admin-posts.html", **context)


# Adding Posts to a database - New
@posts.route("/admin/posts/add", methods=["GET", "POST"])
@login_required
@roles_required(["Admin", "Superadmin"])
def add_post():
    title = "Add New Post"
    form = PostForm(author=current_user.username)

    if form.validate_on_submit():
        headImg = None
        if form.headImg.data:
            headImg = save_head_image(form.headImg.data, form.title.data)
            # headImg = save_picture(form.headImg.data, form.title.data)

        post = Post(
            title=form.title.data,
            subtitle=form.subtitle.data,
            description=form.description.data,
            headImg=headImg,
            slug=form.slug.data,
            language=form.language.data,
            author=form.author.data,
            content=form.content.data,
            isPublished=form.isPublished.data,
        )
        category = Category.query.get(form.category.data)
        post.category = category

        db.session.add(post)
        db.session.commit()
        flash("Post Added", "success")
        return redirect(url_for("posts.all_posts"))

    context = {"pageTitle": title, "form": form, "title": title}

    return render_template("admin/admin-post-create.html", **context)


@posts.route("/admin/posts/update/<int:post_id>", methods=["GET", "POST"])
@login_required
@roles_required(["Admin", "Superadmin"])
def update_post(post_id):
    title = "Update Post"
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    current_headImg = post.headImg

    # Query the Category object associated with the post
    category = Category.query.get(post.category_id)

    if form.validate_on_submit():
        # Update the post object with the form data
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.description = form.description.data
        post.slug = form.slug.data
        post.language = form.language.data
        post.author = form.author.data
        post.content = form.content.data
        post.isPublished = form.isPublished.data
        post.category = Category.query.get(form.category.data)

        # Check if a new image file has been provided
        if form.headImg.data:
            headImg = save_head_image(form.headImg.data, form.title.data)
            post.headImg = headImg
        else:
            post.headImg = current_headImg

        db.session.commit()
        flash("Post Updated", "success")

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
    form.category.data = post.category_id

    context = {
        "pageTitle": title,
        "title": title,
        "form": form,
    }
    return render_template("admin/admin-post-create.html", **context)


# Changing post isPublish to True or False
@posts.route("/admin/posts/publish/<int:post_id>", methods=["GET", "POST"])
@login_required
@roles_required(["Admin", "Superadmin"])
def publish_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.isPublished:
        post.isPublished = False
        flash("Post Drafted", "warning")
    else:
        post.isPublished = True
        flash("Post Published", "success")

    db.session.commit()

    source = request.args.get("source")
    if source == "all_posts":
        return redirect(url_for("posts.all_posts"))
    elif source == "user_details":
        user_id = request.args.get("user_id")
        if user_id is not None:
            return redirect(url_for("users.user_details", user_id=user_id))
    else:
        return redirect(url_for("posts.all_posts"))


# Delete Post - New
@posts.route("/admin/posts/delete/<int:post_id>", methods=["GET", "POST"])
@login_required
@roles_required(["Admin", "Superadmin"])
def delete_post(post_id):
    title = "Delete Post"
    post = Post.query.filter_by(id=post_id).first_or_404()

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Post Deleted", "success")
        source = request.args.get("source")
        if source == "all_posts":
            return redirect(url_for("posts.all_posts"))
        elif source == "user_details":
            user_id = request.args.get("user_id")
            if user_id is not None:
                return redirect(url_for("users.user_details", user_id=user_id))
        else:
            return redirect(url_for("posts.all_posts"))

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
    try:
        user = User.query.filter_by(id=user_id).first_or_404()
        num_deleted = Post.query.filter_by(author=user.username).delete()

        if num_deleted > 0:
            db.session.commit()
            flash(f"Deleted {num_deleted} posts by {user.username}.", "success")
        else:
            flash(f"No posts by {user.username} to delete.", "info")

    except Exception as e:
        flash("An error occurred while deleting posts.", "error")
        db.session.rollback()
        abort(500)

    # Redirect back to the user details page
    return redirect(url_for("users.user_details", user_id=user_id))


# Method that returns total number of posts
@posts.route("/post/number_of_posts", methods=["GET"])
def number_of_posts():
    number_of_posts = Post.query.count()
    return jsonify(number_of_posts=number_of_posts)


# Method that returns total number of posts by each month
@posts.route("/api/posts/count_by_months", methods=["GET"])
def posts_count():
    postsCountList = []

    for x in range(1, 13):
        postsCountList.append(get_posts_count(x))

    return jsonify(postsCountList=postsCountList)


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return "%s%s" % (filename_prefix, str(random.randrange(1000, 10000)))


@posts.route("/ckupload/", methods=["POST", "OPTIONS", "GET"])
def ckupload():
    """CKEditor file upload"""
    error = ""
    url = ""
    callback = request.args.get("CKEditorFuncNum")
    if request.method == "POST" and "upload" in request.files:
        fileobj = request.files["upload"]
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = "%s%s" % (gen_rnd_filename(), fext)
        filepath = os.path.join(app.root_path, "static/upload/media/images", rnd_name)
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = "ERROR_CREATE_DIR"
        elif not os.access(dirname, os.W_OK):
            error = "ERROR_DIR_NOT_WRITEABLE"
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
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response
