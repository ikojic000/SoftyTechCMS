from flaskblog.comments.database_manager import comment_count_in_single_month


# Define a function to get the count of comments for a specific month
def get_comments_count(month):
    """
    Get the count of comments for a specific month.

    Args:
        month (int): The month for which to retrieve the comment count.

    Returns:
        int: The count of comments for the specified month.
    """
    # Call the 'comment_count_in_single_month' function with the provided month
    comment_count = comment_count_in_single_month(month)

    # Return the count of comments
    return comment_count
