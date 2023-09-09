from datetime import datetime
import random
from SoftyTechCMS import app
import os
from PIL import Image
from skimage import io, metrics
from wtforms.validators import ValidationError

from SoftyTechCMS.posts.database_manager import (
    get_post_by_slug_validation,
    get_post_by_subtitle_validation,
    get_post_by_title_validation,
    posts_count_in_single_month,
)


# Method for saving pictures to a folder on a server and returning the picture name
def save_picture(form_picture, title):
    """
    Save an image to a folder on the server and return the picture name.

    Args:
        form_picture (FileStorage): The image file to be saved.
        title (str): The title used for naming the image.

    Returns:
        str: The filename of the saved image.
    """
    # Extract filename and extension from the provided image
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

    # Return the filename of the saved image
    return f"{title}_{filename}{extension}"


# Method for saving images to a folder on a server and returning a unique filename
def save_head_image(image_data, title):
    """
    Save an image to a folder on the server with a unique filename and return the unique filename.

    Args:
        image_data (FileStorage): The image file to be saved.
        title (str): The title used for naming the image.

    Returns:
        str: The unique filename of the saved image or None if the image_data is empty.
    """
    if not image_data:
        return None

    filename = image_data.filename
    extension = os.path.splitext(filename)[1].lower()

    # Build the complete path to save the image
    save_folder = os.path.join(app.root_path, "static/upload/media/images/head_Images")

    if file_exists_in_folder(save_folder, filename):
        print(f"Found an existing image with the same filename: {filename}")
        return filename

    # Read the uploaded image
    uploaded_image = io.imread(image_data)

    # SSIM threshold - how similar images should be - 90%
    ssim_threshold = 0.9

    # Check if an image with similar content already exists using SSIM
    for existing_filename in os.listdir(save_folder):
        print(f"Testing an image with similar content: {existing_filename}")
        existing_path = os.path.join(save_folder, existing_filename)
        existing_image = io.imread(existing_path)

        # Check if the dimensions of the two images are the same
        if uploaded_image.shape != existing_image.shape:
            continue  # Skip this image and continue with the next one

        # Calculate the Structural Similarity Index (SSIM) between the uploaded image and the existing image
        ssim_score = metrics.structural_similarity(
            uploaded_image, existing_image, multichannel=True
        )

        if ssim_score >= ssim_threshold:
            # If SSIM is above or equal to the threshold, return the existing filename
            print(f"Found a similar image with SSIM: {ssim_score}")
            return existing_filename

    # Generate a unique filename using the title and a random hex string
    unique_filename = generate_unique_filename(title, extension)

    # Build the complete path to save the image with the unique filename
    save_path = os.path.join(save_folder, unique_filename)

    # Save the image to the specified path
    # Open the image and save it to the specified path
    image = Image.open(image_data)
    image.save(save_path)

    return unique_filename


# Method to generate a unique filename
def generate_unique_filename(title, extension):
    """
    Generate a unique filename based on the provided title and extension.

    Args:
        title (str): The title used for naming the image.
        extension (str): The file extension (e.g., '.jpg', '.png').

    Returns:
        str: The unique filename.
    """
    return title + "_" + os.urandom(16).hex() + extension


# Method to check if a file with the given filename exists in the folder
def file_exists_in_folder(folder, filename):
    """
    Check if a file with the given filename exists in the specified folder.

    Args:
        folder (str): The folder to check for the file.
        filename (str): The filename to check for.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.isfile(os.path.join(folder, filename))


# Method for generating a random filename prefix
def gen_rnd_filename():
    """
    Generate a random filename prefix.

    Returns:
        str: Random filename prefix.
    """
    filename_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return "%s%s" % (filename_prefix, str(random.randrange(1000, 10000)))


# Method that returns post count in a single month
def get_posts_count(month):
    """
    Get the post count for a single month.

    Args:
        month (int): The month for which to retrieve the post count.

    Returns:
        int: The number of posts in the specified month.
    """
    post_count = posts_count_in_single_month(month)
    return post_count


def validate_title(self, title):
    """
    Custom validation method for the 'title' field.

    Checks if a post with the same title already exists in the database.

    :param title: The title to validate.
    :type title: str
    :raises ValidationError: If a post with the same title exists,
                             raises an error with an appropriate message.
    """

    # Check if a post with the same title already exists
    post = get_post_by_title_validation(title.data)
    if post:
        raise ValidationError(
            "A post with this title already exists. Please choose a different title."
        )


def validate_subtitle(self, subtitle):
    """
    Custom validation method for the 'subtitle' field.

    Checks if a post with the same subtitle already exists in the database.

    :param subtitle: The subtitle to validate.
    :type subtitle: str
    :raises ValidationError: If a post with the same subtitle exists,
                             raises an error with an appropriate message.
    """

    # Check if a post with the same subtitle already exists
    post = get_post_by_subtitle_validation(subtitle.data)
    if post:
        raise ValidationError(
            "A post with this subtitle already exists. Please choose a different subtitle."
        )


def validate_slug(self, slug):
    """
    Custom validation method for the 'slug' field.

    Checks if a post with the same slug already exists in the database.

    :param slug: The slug to validate.
    :type slug: str
    :raises ValidationError: If a post with the same slug exists,
                             raises an error with an appropriate message.
    """

    # Check if a post with the same slug already exists
    post = get_post_by_slug_validation(slug.data)
    if post:
        raise ValidationError(
            "A post with this slug already exists. Please choose a different slug."
        )
