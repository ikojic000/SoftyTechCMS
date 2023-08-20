from flask import render_template, url_for, redirect, flash, request, Blueprint
from flaskblog import app, db, mail
from flaskblog.logs.request_logging import after_request, before_request
from flaskblog.models import Post, Comment, User
from flaskblog.main.forms import SearchForm, ContactForm
from flaskblog.comments.forms import CommentForm
from flask_login import current_user
from flask_mail import Message
import flask_whooshalchemy as wa


main = Blueprint("main", __name__)

main.before_request(before_request)
main.after_request(after_request)

# wa.whoosh_index(app, Post)


# Route for HomePage
# Displaying Posts and Search Function
@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
def home():
    form = SearchForm()

    if form.validate_on_submit():
        search_term = form.search.data
        page = request.args.get("page", 1, type=int)
        query = Post.query.filter_by(isPublished=True).order_by(Post.date_posted.desc())
        search_results = query.whoosh_search(search_term)
        posts = search_results.paginate(page=page, per_page=3)
    else:
        page = request.args.get("page", 1, type=int)
        query = Post.query.filter_by(isPublished=True).order_by(Post.date_posted.desc())
        posts = query.paginate(page=page, per_page=3)

    context = {"posts": posts, "form": form}

    return render_template("index.html", **context)


# Route for AboutPage
@main.route("/about")
def about():
    return render_template("about.html")


# Route for ContactPage


@main.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if current_user.is_authenticated:
        form.name.data = current_user.username
        form.email.data = current_user.email

    if form.validate_on_submit():
        message = Message(
            form.subject.data,
            sender="softythetechguy@gmail.com",
            recipients=["ikojic000@gmail.com"],
        )
        message.body = f"""
        From: {form.name.data} <{form.email.data}>
        {form.message.data}
        """
        mail.send(message)
        flash(
            "Thank you for your message. We will reply as soon as possible!", "success"
        )
        return redirect(url_for("main.home"))

    context = {
        "title": "Contact",
        "form": form,
    }

    return render_template("contact.html", **context)


# Route for Single Post
# Displaying Post by its Slug


@main.route("/<slug>", methods=["GET", "POST"])
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()

    comments = (
        Comment.query.order_by(Comment.date_posted.desc())
        .filter_by(post_id=post.id)
        .all()
    )

    head_img_url = url_for(
        "static", filename=f"upload/media/images/head_Images/{post.headImg}"
    )

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.comment.data, user_id=current_user.id, post_id=post.id
        )
        db.session.add(comment)
        db.session.commit()
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
