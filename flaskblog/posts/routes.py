from flask import render_template, url_for, redirect, flash, request, Blueprint, g
from sqlalchemy.sql import text
from flask.json import jsonify
from flaskblog import app, db, mail
from flaskblog.models import Post, Comment, RequestLog, User
from flaskblog.posts.forms import PostForm, MediaForm
from flask_login import current_user, login_required, logout_user
import flask_whooshalchemy as wa
from flask_user import roles_required
from datetime import datetime
import os
from PIL import Image
import secrets
import random


posts = Blueprint("posts", __name__)


# Dashoard - Table wih all posts with edit/delete buttons - New Design
@posts.route("/admin/posts/all")
@login_required
@roles_required(["Admin", "Superadmin"])
def allPosts():
    posts = Post.query.all()
    title = "All Posts"

    return render_template(
        "admin/admin-posts.html", posts=posts, pageTitle=title, title=title
    )


# Adding Posts to a database - New
@posts.route("/admin/posts/add", methods=["GET", "POST"])
@login_required
@roles_required(["Admin", "Superadmin"])
def add_post():
    title = "Add New Post"
    logged_in_user = current_user
    form = PostForm(author=logged_in_user.username)

    if form.validate_on_submit():
        if form.headImg.data:
            # headImg = save_picture(
            #     form.headImg.data, form.title.data
            # )
            headImg = save_head_image(form.headImg.data, form.title.data)
            post = Post(
                title=form.title.data,
                subtitle=form.subtitle.data,
                description=form.description.data,
                headImg=headImg,
                slug=form.slug.data,
                category=form.category.data,
                language=form.language.data,
                author=form.author.data,
                content=form.content.data,
            )
        else:
            post = Post(
                title=form.title.data,
                subtitle=form.subtitle.data,
                description=form.description.data,
                slug=form.slug.data,
                category=form.category.data,
                language=form.language.data,
                author=form.author.data,
                content=form.content.data,
            )

        db.session.add(post)
        db.session.commit()
        flash("Post Added", "success")
        return redirect(url_for("posts.allPosts"))

    return render_template(
        "admin/admin-add-post.html", pageTitle=title, form=form, title=title
    )


# Updating Post - New
@posts.route("/admin/posts/update/<int:post_id>", methods=["GET", "POST"])
@login_required
@roles_required(["Admin", "Superadmin"])
def update_post(post_id):
    title = "Update Post"
    post = Post.query.filter_by(id=post_id).first()
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.description = form.description.data
        post.slug = form.slug.data
        post.category = form.category.data
        post.language = form.language.data
        post.author = form.author.data
        post.content = form.content.data
        post.isPublished = form.isPublished.data

        db.session.commit()
        flash("Post Updated", "success")
        source = request.args.get("source")
        if source == "all_posts":
            return redirect(url_for("posts.allPosts"))
        elif source == "user_details":
            user_id = request.args.get("user_id")
            if user_id is not None:
                return redirect(url_for("users.user_details", user_id=user_id))
        else:
            return redirect(url_for("posts.allPosts"))

    elif request.method == "GET":
        form.title.data = post.title
        form.subtitle.data = post.subtitle
        form.description.data = post.description
        form.headImg.data = post.headImg
        form.slug.data = post.slug
        form.category.data = post.category
        form.language.data = post.language
        form.author.data = post.author
        form.content.data = post.content
        form.isPublished.data = post.isPublished

    return render_template(
        "admin/admin-add-post.html", pageTitle=title, title=title, form=form
    )


# Changing post isPublish to True or False
@posts.route("/admin/posts/publish/<int:post_id>", methods=["GET", "POST"])
@login_required
@roles_required(["Admin", "Superadmin"])
def publish_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()

    if post.isPublished:
        post.isPublished = False
        db.session.commit()
        flash("Post Drafted", "warning")
    else:
        post.isPublished = True
        db.session.commit()
        flash("Post Published", "success")

    source = request.args.get("source")
    if source == "all_posts":
        return redirect(url_for("posts.allPosts"))
    elif source == "user_details":
        user_id = request.args.get("user_id")
        if user_id is not None:
            return redirect(url_for("users.user_details", user_id=user_id))
    else:
        return redirect(url_for("posts.allPosts"))


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
            return redirect(url_for("posts.allPosts"))
        elif source == "user_details":
            user_id = request.args.get("user_id")
            if user_id is not None:
                return redirect(url_for("users.user_details", user_id=user_id))
        else:
            return redirect(url_for("posts.allPosts"))

    return render_template(
        "admin/admin-delete-post.html", pageTitle=title, title=title, post=post
    )


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


# Logging methods


@posts.before_request
def before_request():
    g.start_time = datetime.utcnow()


@posts.after_request
def after_request(response):
    endpoint = request.endpoint
    method = request.method
    user_id = None

    if current_user.is_authenticated:
        user_id = current_user.id

    timestamp = g.start_time

    # Create a new RequestLog instance
    request_log = RequestLog(
        endpoint=endpoint, methodType=method, user_id=user_id, timestamp=timestamp
    )

    # Add the new request log to the database session
    db.session.add(request_log)

    # Commit the changes to the database
    db.session.commit()

    return response


# Util methods


# Method for saving pictures to a folder on a server and returning picture name
def save_picture(form_picture, title):
    # Extract filename and extension
    filename, extension = os.path.splitext(form_picture.filename)

    # Generate the complete path to save the image
    picture_path = os.path.join(
        app.root_path,
        "static/upload/media/images/head_Images",
        f"{title}_{filename}{extension}",
    )

    # Open the image and save it to the specified path
    image = Image.open(form_picture)
    image.save(picture_path)

    return f"{title}_{filename}{extension}"


# Method for saving pictures to a folder on a server and returning unique picture name
def save_head_image(image_data, title):
    if image_data:
        filename = image_data.filename
        extension = os.path.splitext(filename)[1].lower()

        # Generate a unique filename
        unique_filename = title + "_" + os.urandom(16).hex() + extension

        # Build the complete path to save the image
        save_path = os.path.join(
            app.root_path,
            "static/upload/media/images/head_Images",
            unique_filename,
        )

        # Save the image to the specified path
        image_data.save(save_path)

        return unique_filename
    else:
        return None


# Method that returns post count in a single month
def get_posts_count(month):
    current_year = datetime.utcnow().year
    start_date = datetime(current_year, month, 1)
    if month == 12:
        end_date = datetime(current_year + 1, 1, 1)
    else:
        end_date = datetime(current_year, month + 1, 1)

    post_count = Post.query.filter(
        Post.date_posted >= start_date, Post.date_posted < end_date
    ).count()

    # response = {"month": month, "year": current_year, "post_count": post_count}
    # return jsonify(response)
    return post_count
