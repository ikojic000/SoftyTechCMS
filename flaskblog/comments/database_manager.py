from datetime import datetime
from flask import flash, abort
from flaskblog.models import Post, User, Comment
from flaskblog import db


# Get all comments along with associated user and post
def get_all_comments():
    """
    Get all comments along with their associated user and post information.

    Returns:
        list: A list of Comment objects with associated User and Post objects.
    """
    return (
        Comment.query.join(
            User, Comment.user_id == User.id
        )  # Join Comment and User tables
        .join(Post, Comment.post_id == Post.id)  # Join Comment and Post tables
        .all()  # Retrieve all comments
    )


# Retrieve a comment by its ID.
def get_comment_by_id(comment_id):
    """
    Retrieve a comment by its unique identifier.

    Args:
        comment_id (int): The unique identifier (ID) of the comment to retrieve.

    Returns:
        Comment or None: The Comment object with the specified ID if found, or None if not found.
    """
    return Comment.query.get(comment_id)


# Get comments for a specific post ID, ordered by date posted
def comments_by_post_id(post_id):
    """
    Get comments for a specific post ID, ordered by date posted.

    Args:
        post_id (int): The ID of the post for which to retrieve comments.

    Returns:
        list: A list of Comment objects for the specified post, ordered by date posted.
    """
    return (
        Comment.query.order_by(
            Comment.date_posted.desc()
        )  # Order comments by date posted in descending order
        .filter_by(post_id=post_id)  # Filter comments by the specified post ID
        .all()  # Retrieve all matching comments
    )


# Get comments associated with a specific user
def get_comments_by_user_id(user_id):
    """
    Get comments associated with a specific user.

    Args:
        user_id (int): The ID of the user for whom to retrieve comments.

    Returns:
        list: A list of Comment objects associated with the specified user.
    """
    return (
        Comment.query.join(
            User, Comment.user_id == User.id
        )  # Join Comment and User tables
        .join(Post, Comment.post_id == Post.id)  # Join Comment and Post tables
        .filter(Comment.user_id == user_id)  # Filter comments by the specified user ID
        .all()  # Retrieve all matching comments
    )


# Delete a comment by its ID
def delete_comment_by_id(comment_id):
    """
    Delete a comment by its ID.

    Args:
        comment_id (int): The ID of the comment to be deleted.

    Returns:
        None
    """
    try:
        comment = Comment.query.filter_by(
            id=comment_id
        ).first_or_404()  # Find the comment by its ID
        db.session.delete(comment)  # Delete the comment from the database
        db.session.commit()  # Commit the transaction
    except Exception as e:
        flash(
            "An error occurred while deleting the comment.", "error"
        )  # Display an error message
        db.session.rollback()  # Rollback the transaction
        abort(
            500, "An error occurred while deleting the comment. Please try again later."
        )  # Abort the request with a 500 Internal Server Error


# Add a new comment
def add_comment(content, user_id, post_id):
    """
    Add a new comment.

    Args:
        content (str): The content of the comment.
        user_id (int): The ID of the user who posted the comment.
        post_id (int): The ID of the post to which the comment belongs.

    Returns:
        None
    """
    try:
        comment = Comment(
            content=content, user_id=user_id, post_id=post_id
        )  # Create a new comment object
        db.session.add(comment)  # Add the comment to the database session
        db.session.commit()  # Commit the transaction
    except Exception as e:
        flash(
            "An error occurred while adding the comment.", "error"
        )  # Display an error message
        db.session.rollback()  # Rollback the transaction
        abort(
            500, "An error occurred while adding the comment. Please try again later."
        )  # Abort the request with a 500 Internal Server Error


# Delete all comments by a specific user
def delete_all_users_comments(user_id):
    """
    Delete all comments by a specific user.

    Args:
        user_id (int): The ID of the user whose comments should be deleted.

    Returns:
        None
    """
    try:
        user = User.query.filter_by(
            id=user_id
        ).first_or_404()  # Find the user by their ID
        num_deleted = Comment.query.filter_by(
            user_id=user_id
        ).delete()  # Delete all comments by the user

        if num_deleted > 0:
            db.session.commit()  # Commit the transaction
            flash(
                f"Deleted {num_deleted} comments by {user.username}.", "success"
            )  # Display a success message
        else:
            flash(
                f"No comments by {user.username} to delete.", "info"
            )  # Display an informational message

    except Exception as e:
        flash(
            "An error occurred while deleting comments.", "error"
        )  # Display an error message
        db.session.rollback()  # Rollback the transaction
        abort(
            500, "An error occurred while deleting comments. Please try again later."
        )  # Abort the request with a 500 Internal Server Error


# Get the total count of comments
def count_comments():
    """
    Get the total count of comments.

    Returns:
        int: The total count of comments.
    """
    return Comment.query.count()  # Count the total number of comments


# Get the count of comments in a specific month
def comment_count_in_single_month(month):
    """
    Get the count of comments in a specific month.

    Args:
        month (int): The month for which to retrieve the comment count.

    Returns:
        int: The count of comments for the specified month.
    """
    current_year = datetime.utcnow().year
    start_date = datetime(
        current_year, month, 1
    )  # Calculate the start date of the month

    if month == 12:
        end_date = datetime(
            current_year + 1, 1, 1
        )  # Calculate the end date of December
    else:
        end_date = datetime(
            current_year, month + 1, 1
        )  # Calculate the end date of the next month

    return Comment.query.filter(
        Comment.date_posted >= start_date,
        Comment.date_posted < end_date,  # Filter comments by date range
    ).count()  # Count the comments in the specified month
