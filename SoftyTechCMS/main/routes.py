from flask import render_template, url_for, redirect, flash, request, Blueprint, abort
from flask_login import current_user

from SoftyTechCMS import app
from SoftyTechCMS.comments.database_manager import add_comment, comments_by_post_id
from SoftyTechCMS.comments.forms import CommentForm
from SoftyTechCMS.comments.utils import comment_user_matches_current_user
from SoftyTechCMS.logs.request_logging import after_request, before_request
from SoftyTechCMS.main.forms import SearchForm, ContactForm
from SoftyTechCMS.main.utils import send_mail
from SoftyTechCMS.posts.database_manager import (
    get_post_by_slug,
    get_posts_pagination,
    get_posts_searched_pagination,
)

# Create a Blueprint for the main routes
main = Blueprint("main", __name__)

# Register before and after request handlers for logging
main.before_request(before_request)
main.after_request(after_request)

# Add 'comment_user_matches_current_user' function to the Jinja templates, making it available for rendering
app.jinja_env.globals.update(
    comment_user_matches_current_user=comment_user_matches_current_user
)


@main.route("/test_error")
def test_error():
    print("Test error - 500")
    abort(500, "Test error message")


# Home page route
@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
def home():
    """
    Display the home page, including a list of posts.

    Returns:
        render_template: Renders the home page template.
    """
    # Create a search form
    form = SearchForm()

    # Check if the form is submitted and validate it
    if form.validate_on_submit():
        posts = get_posts_searched_pagination(request, 5, form.search.data)
    else:
        posts = get_posts_pagination(request, 5)

    context = {"posts": posts, "form": form}

    return render_template("index.html", **context)


# About page route
@main.route("/about")
def about():
    """
    Display the about page.

    Returns:
        render_template: Renders the about page template.
    """
    return render_template("about.html")


# About page route
@main.route("/about/MPDTech")
def about_mpd_tech():
    """
    Display the MPD Tech about page.

    Returns:
        render_template: Renders the about-mpd-tech page template.
    """
    return render_template("about-mpd-tech.html")


# Contact page route
@main.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Display the contact page and handle contact form submissions.

    Returns:
        render_template or redirect: Renders the contact page template or redirects to the home page.
    """
    form = ContactForm()

    # Pre-fill form fields if user is authenticated
    if current_user.is_authenticated:
        form.name.data = current_user.username
        form.email.data = current_user.email

    if form.validate_on_submit():
        send_mail(form.subject.data, form.name.data, form.email.data, form.message.data)
        flash(
            "Thank you for your message. We will reply as soon as possible!", "success"
        )
        return redirect(url_for("main.home"))

    context = {
        "title": "Contact",
        "form": form,
    }

    return render_template("/form-templates/contact.html", **context)


# Individual post page route
@main.route("/<slug>", methods=["GET", "POST"])
def post(slug):
    """
    Display an individual blog post page, including comments and a comment submission form.

    Args:
        slug (str): The unique slug of the post.

    Returns:
        render_template or redirect: Renders the post page template or redirects to the home page.
    """
    post = get_post_by_slug(slug)

    comments = comments_by_post_id(post.id)

    head_img_url = url_for(
        "static", filename=f"upload/media/images/head_Images/{post.headImg}"
    )

    form = CommentForm()
    if form.validate_on_submit():
        add_comment(form.comment.data, current_user.id, post.id)
        flash("Comment added", "success")
        return redirect(url_for("main.post", slug=post.slug))

    context = {
        "title": post.title,
        "post": post,
        "comments": comments,
        "form": form,
        "headImg": head_img_url,
    }

    return render_template("post.html", **context)
