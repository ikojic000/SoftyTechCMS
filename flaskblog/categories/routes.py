from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required
from flask_user import roles_required
from flaskblog.categories.forms import CategoryForm
from flaskblog.logs.request_logging import after_request, before_request
from flaskblog import db
from flaskblog.models import Category

categories = Blueprint("categories", __name__)

categories.before_request(before_request)
categories.after_request(after_request)


@categories.route("/admin/categories/all")
@login_required
@roles_required(["Admin", "Superadmin"])
def all_categories():
    title = "All Categories"
    categories = Category.query.all()
    form = CategoryForm()
    context = {
        "title": title,
        "pageTitle": title,
        "categories": categories,
        "form": form,
    }
    return render_template("admin/admin-categories.html", **context)


# Deleting Comments - New Design
@categories.route("/admin/categories/delete/<int:category_id>")
@login_required
@roles_required(["Admin", "Superadmin"])
def delete_category(category_id):
    category = Category.query.filter_by(id=category_id).first_or_404()
    db.session.delete(category)
    db.session.commit()
    flash("You have deleted the category!", "success")

    return redirect(url_for("categories.all_categories"))


# Route for adding categories
@categories.route("/admin/categories/add", methods=["POST"])
@login_required
@roles_required(["Admin", "Superadmin"])
def add_category():
    form = CategoryForm()

    if form.validate_on_submit():
        category_name = form.category.data

        # Check if the category already exists
        existing_category = Category.query.filter_by(name=category_name).first()

        if not existing_category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()
            flash("Category added successfully", "success")
        else:
            flash("Category already exists", "warning")

    return redirect(url_for("categories.all_categories"))
