
from flask import render_template, url_for, redirect, flash, request, Blueprint
from flaskblog import app, db, mail
from flaskblog.models import Post, Comment, User
from flaskblog.posts.forms import PostForm, MediaForm
from flask_login import current_user, login_required, logout_user
import flask_whooshalchemy as wa
from flask_user import roles_required
import os
from PIL import Image
import secrets
import datetime
import random


posts = Blueprint('posts', __name__)



def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))






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


@posts.route('/ckupload/', methods=['POST', 'OPTIONS', 'GET'])
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
@posts.route("/admin/add", methods=['GET', 'POST'])
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
        return redirect(url_for('users.admin'))
    return render_template('admin_addPost.html', title='AddPosts', form=form)


# Deleting Posts from the database
@posts.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('users.admin'))



# Updating Posts in the database
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('users.admin'))
        
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
@posts.route("/admin/media", methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def media():
    form = MediaForm()
    if form.validate_on_submit():
        if form.mediaFile.data:
            media_File = save_picture(form.mediaFile.data)
            flash('Upload Successfull!', 'success')
            return redirect(url_for('posts.media'))
    images = os.listdir('flaskblog\static\media\images')
    images_urls = []
    for image in images:
        images_urls.append(url_for('static', filename='media/images/' + image))
    return render_template('admin_Media.html', title='Media', form=form, image_names=images_urls)