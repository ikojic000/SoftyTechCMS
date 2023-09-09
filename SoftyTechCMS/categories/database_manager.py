from flask import flash, abort

from SoftyTechCMS import db
from SoftyTechCMS.models import Category


# Get all categories from the database
def get_all_categories():
    """
    Retrieve all categories from the database.

    Returns:
        list of Category: List of Category objects.
    """
    return Category.query.all()


# Delete a category by its ID
def delete_category_by_id(category_id):
    """
    Delete a category by its ID.

    Args:
        category_id (int): The ID of the category to be deleted.
    """
    try:
        # Get the category by its ID, or return a 404 error if not found
        category = Category.query.get_or_404(category_id)

        # Find the default category with id = 1
        default_category = Category.query.get(1)

        # Update the posts associated with the category to have the default category
        for post in category.posts:
            post.category = default_category

        # Delete the category from the database
        db.session.delete(category)
        db.session.commit()
    except Exception as e:
        flash("An error occurred while deleting the category.", "error")
        db.session.rollback()
        abort(
            500,
            "An error occurred while deleting the category. Please try again later.",
        )


# Create a new category with the given name
def create_category(category_name):
    """
    Create a new category with the given name.

    Args:
        category_name (str): The name of the new category.
    """
    try:
        # Check if a category with the same name already exists
        existing_category = Category.query.filter_by(name=category_name).first()

        if not existing_category:
            # If the category doesn't exist, create it and add it to the database
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()
            flash("Category added successfully", "success")
        else:
            # If a category with the same name exists, show a warning message
            flash("Category already exists", "warning")
    except Exception as e:
        flash("An error occurred while creating the category.", "error")
        db.session.rollback()
        abort(
            500,
            "An error occurred while creating the category. Please try again later.",
        )
