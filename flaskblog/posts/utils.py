from datetime import datetime
import random
from flaskblog import app
import os
from PIL import Image

from flaskblog.models import Post


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


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return "%s%s" % (filename_prefix, str(random.randrange(1000, 10000)))


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
