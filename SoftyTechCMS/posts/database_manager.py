from datetime import datetime
from flask import flash, abort
from sqlalchemy import or_
from SoftyTechCMS import db
from SoftyTechCMS.models import Category, Post
from SoftyTechCMS.users.database_manager import get_user_by_id


# Get a post by its slug (unique identifier)
def get_post_by_slug(slug):
    """
    Retrieve a post from the database by its slug.

    Args:
        slug (str): The slug of the post.

    Returns:
        Post: The Post object if found, else a 404 error is raised.
    """
    return Post.query.filter_by(slug=slug).first_or_404()


# Get posts with pagination
def get_posts_pagination(request, per_page):
    """
    Retrieve a paginated list of published posts ordered by date posted.

    Args:
        request: The Flask request object.
        per_page (int): Number of posts per page.

    Returns:
        Pagination: A Pagination object containing the posts.
    """
    page = request.args.get("page", 1, type=int)
    query = Post.query.filter_by(isPublished=True).order_by(Post.date_posted.desc())
    return query.paginate(page=page, per_page=per_page)


# Get paginated search results
def get_posts_searched_pagination(request, per_page, search_term):
    """
    Retrieve paginated search results for posts.

    Args:
        request: The Flask request object.
        per_page (int): Number of search results per page.
        search_term (str): The term to search for in posts.

    Returns:
        Pagination: A Pagination object containing the search results.
    """
    page = request.args.get("page", 1, type=int)

    # Construct a query that searches multiple columns using 'LIKE' operator
    query = Post.query.filter(
        Post.isPublished == True,  # Filter for published posts
        or_(
            Post.title.like(f"%{search_term}%"),
            Post.subtitle.like(f"%{search_term}%"),
            Post.description.like(f"%{search_term}%"),
            Post.content.like(f"%{search_term}%"),
            Post.category.has(Category.name.like(f"%{search_term}%")),
            Post.author.like(f"%{search_term}%"),
        ),
    ).order_by(Post.date_posted.desc())

    # Paginate the results
    search_results = query.paginate(page=page, per_page=per_page)

    return search_results


# Get all posts
def get_all_posts():
    """
    Retrieve all posts from the database.

    Returns:
        list of Post: List of Post objects.
    """
    return Post.query.all()


# Method for creating new post
def create_post(
    title,
    subtitle,
    description,
    headImg,
    slug,
    language,
    author,
    content,
    isPublished,
    category,
):
    """
    Create a new post and add it to the database.

    Args:
        title (str): The title of the post.
        subtitle (str): The subtitle of the post.
        description (str): The description of the post.
        headImg (str): The URL of the post's header image.
        slug (str): The slug for the post's URL.
        language (str): The language of the post.
        author (str): The author of the post.
        content (str): The content of the post.
        isPublished (bool): Whether the post is published.
        category: The category associated with the post.

    Returns:
        None
    """
    try:
        post = Post(
            title=title,
            subtitle=subtitle,
            description=description,
            headImg=headImg,
            slug=slug.lower().replace(" ", "-"),
            language=language,
            author=author,
            content=content,
            isPublished=isPublished,
        )
        post.category = category

        db.session.add(post)
        db.session.commit()
        flash("Post created successfully", "success")
    except Exception as e:
        flash("An error occurred while saving the post to the database.", "error")
        db.session.rollback()
        abort(
            500,
            "An error occurred while saving the post to the database. Please try again later.",
        )


def publish_unpublish_post(post_id):
    """
    Publish or unpublish a post by toggling its "isPublished" attribute.

    Args:
        post_id (int): The ID of the post to be published/unpublished.

    Returns:
        None
    """
    try:
        post = Post.query.get_or_404(post_id)

        if post.isPublished:
            post.isPublished = False
            flash("Post Drafted", "warning")
        else:
            post.isPublished = True
            flash("Post Published", "success")

        db.session.commit()
    except Exception as e:
        flash("An error occurred while publishing/unpublishing the post.", "error")
        db.session.rollback()
        abort(
            500,
            "An error occurred while publishing/unpublishing the post. Please try again later.",
        )


# Get a post by its ID
def get_post_by_id(post_id):
    """
    Retrieve a post from the database by its ID.

    Args:
        post_id (int): The ID of the post.

    Returns:
        Post: The Post object if found, else a 404 error is raised.
    """
    return Post.query.filter_by(id=post_id).first_or_404()


# Get posts by author
def get_posts_by_author(author):
    """
    Retrieve all posts by a specific author.

    Args:
        author (str): The username of the author.

    Returns:
        list of Post: List of Post objects.
    """
    return Post.query.filter_by(author=author).all()


def post_delete(post):
    """
    Delete a post from the database.

    Args:
        post (Post): The Post object to be deleted.

    Returns:
        None
    """
    try:
        db.session.delete(post)
        db.session.commit()
    except Exception as e:
        flash("An error occurred while deleting the post.", "error")
        db.session.rollback()
        abort(500, "An error occurred while deleting the post. Please try again later.")


# Delete all posts by a user
def delete_all_users_posts(user_id):
    """
    Delete all posts by a specific user.

    Args:
        user_id (int): The ID of the user whose posts should be deleted.

    Returns:
        None
    """
    try:
        user = get_user_by_id(user_id)
        num_deleted = Post.query.filter_by(author=user.username).delete()

        if num_deleted > 0:
            db.session.commit()
            flash(f"Deleted {num_deleted} posts by {user.username}.", "success")
        else:
            flash(f"No posts by {user.username} to delete.", "info")

    except Exception as e:
        flash("An error occurred while deleting posts.", "error")
        db.session.rollback()
        abort(500, "An error occurred while deleting posts. Please try again later.")


# Count the total number of posts
def count_posts():
    """
    Count the total number of posts in the database.

    Returns:
        int: The total number of posts.
    """
    return Post.query.count()


# Count the number of posts in a specific month
def posts_count_in_single_month(month):
    """
    Count the number of posts published in a specific month.

    Args:
        month (int): The month for which to count posts (1-12).

    Returns:
        int: The number of posts published in the specified month.
    """
    current_year = datetime.utcnow().year
    start_date = datetime(current_year, month, 1)
    if month == 12:
        end_date = datetime(current_year + 1, 1, 1)
    else:
        end_date = datetime(current_year, month + 1, 1)

    return Post.query.filter(
        Post.date_posted >= start_date, Post.date_posted < end_date
    ).count()


def get_post_by_subtitle_validation(subtitle):
    """
    Retrieve a post from the database by its subtitle.

    :param subtitle: The subtitle of the post to retrieve.
    :type subtitle: str
    :return: The first post found with the specified subtitle, or None if not found.
    :rtype: Post or None
    """
    return Post.query.filter_by(subtitle=subtitle).first()


def get_post_by_title_validation(title):
    """
    Retrieve a post from the database by its title.

    :param title: The title of the post to retrieve.
    :type title: str
    :return: The first post found with the specified title, or None if not found.
    :rtype: Post or None
    """
    return Post.query.filter_by(title=title).first()


def get_post_by_slug_validation(slug):
    """
    Retrieve a post from the database by its slug.

    :param slug: The slug of the post to retrieve.
    :type slug: str
    :return: The first post found with the specified slug, or None if not found.
    :rtype: Post or None
    """
    return Post.query.filter_by(slug=slug).first()
