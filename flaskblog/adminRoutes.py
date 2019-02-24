# PYTHON FILE WITH / FOR ADMIN SIDE ROUTES

# Imports
from flask import render_template, url_for, redirect, flash, request, make_response
from flaskblog import app, db, bcrypt
from flaskblog.forms import LoginForm, PostForm, RegisterForm, MediaForm, UpdateAccountForm, UpdateAccountRoleForm
from flaskblog.models import User, Post, UserRoles
from flask_login import login_user, logout_user, current_user, login_required
from flask_user import roles_required
import os
from PIL import Image
import secrets
import datetime
import random


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


# Admin HomePage
@app.route("/admin")
@login_required
@roles_required('Admin')
def admin():
    users = User.query.all()
    posts = Post.query.all()
    return render_template('admin_home.html', users=users, posts=posts)


# Registering to a website
# Admin and User side Route
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('automaticRole', user_id = user.id))
    return render_template('register.html', title='Register', form=form)

# Automatically giving role 'reader' when registered
@app.route("/register/<int:user_id>/role", methods=['GET', 'POST'])
def automaticRole(user_id):
    user = User.query.filter_by(id=user_id).first()
    user_role = UserRoles(user_id=user_id, role_id='1')
    db.session.add(user_role)
    db.session.commit()
    return redirect(url_for('login'))


# Logging into a website
# Admin and User side Route
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print("login12345")
            login_user(user)
            next_page = request.args.get('next')
            flash('Logged In!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Failed! Please check your email and password', 'danger')
    return render_template('admin_Login.html', title='Login', form=form)


# Logging out User
# Admin and User side Route
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


# Displaying users in a table
@app.route("/admin/users")
@login_required
@roles_required('Admin')
def users():
    users = User.query.all()
    return render_template('admin_Users.html', users=users)


# Deleting User from the database
@app.route("/user/<int:user_id>/delete", methods=['GET'])
@login_required
@roles_required('Admin')
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted!', 'success')
    return redirect(url_for('users'))


# Updating User in the database
@app.route("/user/<int:user_id>/update", methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    user_role = UserRoles.query.filter_by(user_id=user.id).first()
    form = UpdateAccountRoleForm()
    if form.validate_on_submit():
        user_role.role_id = form.role.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users'))
    elif request.method == 'GET':
        form.role.data = user_role.role_id
    return render_template('userAccountUpdate.html', form=form, user=user)



# Function for saving pictures to a databse and a folder
# Cleaning the code
def save_picture(form_picture):
    print(form_picture)
    print(form_picture.filename)
    f_name, f_ext = os.path.splitext(form_picture.filename)

    picture_fn = f_name + f_ext
    picture_path = os.path.join(app.root_path, 'static/media/images', picture_fn)
    print(picture_path)

    i = Image.open(form_picture)
    print(i)
    i.save(picture_path)

    return picture_fn


@app.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        filepath = os.path.join(app.root_path, 'static/upload', rnd_name)
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
            print(url)
    else:
        error = 'post error'
    res = """<script type="text/javascript"> 
             window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
             </script>""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


# Adding Posts to a database
@app.route("/admin/add", methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def add():
    form = PostForm()
    if form.validate_on_submit():
        if form.headImg.data:
            headImg = save_picture(form.headImg.data)
            post = Post(title=form.title.data, subtitle=form.subtitle.data, description=form.description.data,headImg=headImg, slug=form.slug.data, category=form.category.data, language=form.language.data, author=form.author.data, content=form.content.data)
        else:
            post = Post(title=form.title.data, subtitle=form.subtitle.data, description=form.description.data, slug=form.slug.data, category=form.category.data, language=form.language.data, author=form.author.data, content=form.content.data)
        
        db.session.add(post)
        db.session.commit()
        flash('Post Added', 'success')
        return redirect(url_for('admin'))
    return render_template('admin_addPost.html', title='AddPosts', form=form)


# Deleting Posts from the database
@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('admin'))



# Updating Posts in the database
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def update_post(post_id):
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

        db.session.commit()
        flash('Post Updated', 'success')
        return redirect(url_for('admin'))
        
    elif request.method == 'GET':
        form.title.data = post.title
        form.subtitle.data = post.subtitle
        form.description.data = post.description
        form.headImg.data = post.headImg
        form.slug.data = post.slug
        form.category.data = post.category
        form.language.data = post.language
        form.author.data = post.author
        form.content.data = post.content

    return render_template('admin_addPost.html', title='UpdatePost', form=form)





# Uploading media to a folder on a server
# Displaying preview of those images so Admin can know what was uploaded
@app.route("/admin/media", methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def media():
    form = MediaForm()
    if form.validate_on_submit():
        if form.mediaFile.data:
            media_File = save_picture(form.mediaFile.data)
            flash('Upload Successfull!', 'success')
            return redirect(url_for('media'))
    images = os.listdir('flaskblog\static\media\images')
    images_urls = []
    for image in images:
        images_urls.append(url_for('static', filename='media/images/' + image))
    return render_template('admin_Media.html', title='Media', form=form, image_names=images_urls)



