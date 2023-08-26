from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from flask_user import roles_required
from flaskblog.categories.database_manager import (
    create_category,
    delete_category_by_id,
    get_all_categories,
)
from flaskblog.categories.forms import CategoryForm
from flaskblog.logs.request_logging import after_request, before_request

# Create a Blueprint for managing categories
categories = Blueprint("categories", __name__)

# Register before and after request handlers for logging
categories.before_request(before_request)
categories.after_request(after_request)


# Route to display all categories (admin view)
@categories.route("/admin/categories/all")
@login_required
@roles_required(["Admin", "Superadmin"])
def all_categories():
    """
    Display all categories in a table with the option to add or delete categories.

    Returns:
        render_template: Renders the admin-categories.html template.
    """
    title = "All Categories"

    # Retrieve all categories from the database
    categories_data = get_all_categories()

    # Create a CategoryForm instance for adding new categories
    form = CategoryForm()

    # Define the context for rendering the template
    context = {
        "title": title,
        "pageTitle": title,
        "categories": categories_data,
        "form": form,
    }

    # Render the admin-categories.html template with the specified context
    return render_template("admin/admin-categories.html", **context)


# Route to delete a category by ID (admin view)
@categories.route("/admin/categories/delete/<int:category_id>")
@login_required
@roles_required(["Admin", "Superadmin"])
def delete_category(category_id):
    """
    Delete a category by its ID.

    Args:
        category_id (int): The ID of the category to be deleted.

    Returns:
        redirect: Redirects back to the all_categories route after deleting the category.
    """

    # Call the delete_category_by_id function to delete the category by its ID
    delete_category_by_id(category_id)

    # Flash a success message
    flash("You have deleted the category!", "success")

    # Redirect back to the 'all_categories' route
    return redirect(url_for("categories.all_categories"))


# Route to add a category (admin view)
@categories.route("/admin/categories/add", methods=["POST"])
@login_required
@roles_required(["Admin", "Superadmin"])
def add_category():
    """
    Add a new category.

    Returns:
        redirect: Redirects back to the all_categories route after adding the category.
    """

    # Create a CategoryForm instance
    form = CategoryForm()

    # Check if the form is submitted and valid
    if form.validate_on_submit():
        # Get the category name from the form
        category_name = form.category.data

        # Call the create_category function to add the new category
        create_category(category_name)

    # Redirect back to the 'all_categories' route
    return redirect(url_for("categories.all_categories"))
