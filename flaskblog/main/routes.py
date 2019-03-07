
from flask import render_template, url_for, redirect, flash, request, Blueprint
from flaskblog import app, db, mail
from flaskblog.models import Post, Comment, User
from flaskblog.main.forms import CommentForm, SearchForm, ContactForm
from flask_login import current_user
from flask_mail import Message
import flask_whooshalchemy as wa
import os
import secrets
import datetime
import random


main = Blueprint('main', __name__)

wa.whoosh_index(app, Post)

# Route for HomePage
# Displaying Posts and Search Function
@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if request.method == "POST":
        if form.validate_on_submit:
            print("searching")
            posts = Post.query.whoosh_search(form.search.data).all()
            news = Post.query.order_by(Post.date_posted.desc()).filter_by(category="News").first()
            reviews = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Reviews").first()
            commentary = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Commentary").first()
            print("applying")
            print(posts)
            return render_template('search.html', posts=posts, news=news, reviews=reviews, commentary=commentary, form=form)
    else:
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=1)
        news = Post.query.order_by(Post.date_posted.desc()).filter_by(category="News").first()
        reviews = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Reviews").first()
        commentary = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Commentary").first()
        form.search.data = ''
    return render_template('index.html', posts=posts, page=page, news=news, reviews=reviews, commentary=commentary, title='Home', form=form)


# Route for AboutPage
@main.route("/about")
def about():
    return render_template('about.html')

# Route for ContactPage
@main.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if current_user.is_authenticated:
        form.name.data = current_user.username
        form.email.data = current_user.email

    if form.validate_on_submit():
        message = Message(form.subject.data, sender='softythetechguy@gmail.com', recipients=['ikojic000@gmail.com'])
        message.body = """
        From: %s <%s>
        %s
        """ % (form.name.data, form.email.data, form.message.data)
        mail.send(message)
        flash('Thank you for your message. We will reply as soon as possible!', 'success')
        return redirect(url_for('main.home'))
    return render_template('contact.html', title='Contact', form=form)





# Route for NewsPage
# Displaying only News Category from database
@main.route("/news")
def news():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="News").order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    reviews = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Reviews").first()
    commentary = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Commentary").first()
    return render_template('news.html', title='News', posts=posts, reviews=reviews, commentary=commentary)

# Route for ReviewsPage
# Displaying only Reviews Category from database
@main.route("/reviews")
def reviews():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="Reviews").order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    news = Post.query.order_by(Post.date_posted.desc()).filter_by(category="News").first()
    commentary = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Commentary").first()
    return render_template('reviews.html', title='Reviews', posts=posts, news=news, commentary=commentary, reviews=reviews)

# Route for CommentaryPage
# Displaying only Commentary Category from database
@main.route("/commentary")
def commentary():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="Commentary").order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    news = Post.query.order_by(Post.date_posted.desc()).filter_by(category="News").first()
    reviews = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Reviews").first()
    return render_template('commentary.html', title='Commentary', posts=posts, news=news, reviews=reviews)

# Route for Single Post
# Displaying Post by its Slug
@main.route("/<slug>", methods=['GET', 'POST'])
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    news = Post.query.order_by(Post.date_posted.desc()).filter_by(category="News").first()
    reviews = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Reviews").first()
    commentary = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Commentary").first()
    comments = Comment.query.order_by(Comment.date_posted.desc()).filter_by(post_id=post.id).all()
    headImg = url_for('static', filename='upload/media/images/head_Images/' + post.headImg )
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.comment.data, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added', 'success')
        return redirect(url_for('main.post',slug=post.slug))
    print("slika: " + post.headImg)
    print("lokacija: " + headImg)
    return render_template('post.html', title=post.title, post=post, news=news, reviews=reviews, commentary=commentary, comments=comments, form=form, headImg = headImg )

