# PYTHON FILE WITH / FOR USER SIDE ROUTES

# Imports
from flask import render_template, url_for, redirect, flash, request
from flaskblog import app, db, mail
from flaskblog.models import Post, Comment, User
from flaskblog.forms import UpdateAccountForm, CommentForm, SearchForm, ContactForm
from flask_login import current_user, login_required, logout_user
from flask_mail import Message
import flask_whooshalchemy as wa
import os

wa.whoosh_index(app, Post)

# Route for HomePage
# Displaying Posts and Search Function
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
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
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
        news = Post.query.order_by(Post.date_posted.desc()).filter_by(category="News").first()
        reviews = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Reviews").first()
        commentary = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Commentary").first()
        form.search.data = ''
    return render_template('index.html', posts=posts, page=page, news=news, reviews=reviews, commentary=commentary, title='Home', form=form)


# Route for AboutPage
@app.route("/about")
def about():
    return render_template('about.html')

# Route for ContactPage
@app.route("/contact", methods=['GET', 'POST'])
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
        return redirect(url_for('home'))
    return render_template('contact.html', title='Contact', form=form)


# Route for User Account 
# Displaying user account details and updating account function
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', form=form, title=current_user.username)


@app.route("/account/<int:user_id>/delete", methods=['GET'])
@login_required
def delete_account(user_id):
    print(user_id)
    logout_user()
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash('You have deleted your account..', 'success')
    return redirect(url_for('home'))


# Route for NewsPage
# Displaying only News Category from database
@app.route("/news")
def news():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="News").order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    reviews = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Reviews").first()
    commentary = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Commentary").first()
    return render_template('news.html', title='News', posts=posts, reviews=reviews, commentary=commentary)

# Route for ReviewsPage
# Displaying only Reviews Category from database
@app.route("/reviews")
def reviews():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="Reviews").order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    news = Post.query.order_by(Post.date_posted.desc()).filter_by(category="News").first()
    commentary = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Commentary").first()
    return render_template('reviews.html', title='Reviews', posts=posts, news=news, commentary=commentary, reviews=reviews)

# Route for CommentaryPage
# Displaying only Commentary Category from database
@app.route("/commentary")
def commentary():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="Commentary").order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    news = Post.query.order_by(Post.date_posted.desc()).filter_by(category="News").first()
    reviews = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Reviews").first()
    return render_template('commentary.html', title='Commentary', posts=posts, news=news, reviews=reviews)

# Route for Single Post
# Displaying Post by its Slug
@app.route("/<slug>", methods=['GET', 'POST'])
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    news = Post.query.order_by(Post.date_posted.desc()).filter_by(category="News").first()
    reviews = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Reviews").first()
    commentary = Post.query.order_by(Post.date_posted.desc()).filter_by(category="Commentary").first()
    comments = Comment.query.order_by(Comment.date_posted.desc()).filter_by(post_id=post.id).all()
    headImg = url_for('static', filename='media/images/' + post.headImg )
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.comment.data, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added', 'success')
        return redirect(url_for('post',slug=post.slug))
    print("slika: " + post.headImg)
    print("lokacija: " + headImg)
    return render_template('post.html', title=post.title, post=post, news=news, reviews=reviews, commentary=commentary, comments=comments, form=form, headImg = headImg )


