from datetime import datetime
from flask import Blueprint, redirect, render_template, flash, url_for, request, abort
from flask.json import jsonify
from flask_login import login_required
from flask_user import roles_required
from flaskblog.logs.request_logging import after_request, before_request
from flaskblog.models import Post, Comment, User
from flaskblog import db

comments = Blueprint("comments", __name__)

comments.before_request(before_request)
comments.after_request(after_request)


# Dashoard - Table wih all posts with edit/delete buttons - New Design
@comments.route("/admin/comments/all")
@login_required
@roles_required(["Admin", "Superadmin"])
def all_comments():
    title = "All Comments"
    comments = (
        Comment.query.join(User, Comment.user_id == User.id)
        .join(Post, Comment.post_id == Post.id)
        .all()
    )

    context = {"pageTitle": title, "comments": comments}

    return render_template("admin/admin-comments.html", **context)


# Deleting Comments - New Design
@comments.route("/admin/comments/delete/<int:comment_id>")
@login_required
@roles_required(["Admin", "Superadmin"])
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first_or_404()
    db.session.delete(comment)
    db.session.commit()
    flash("You have deleted the comment!", "success")

    # Get the referrer (URL that the request came from)
    referrer = request.referrer

    # If the referrer is None (e.g., direct access to the delete URL),
    # then redirect to a default page
    if referrer is None:
        return redirect(url_for("posts.allComments"))

    # Otherwise, redirect back to the referrer
    return redirect(referrer)


# Route to delete all comments by a specific user
@comments.route("/admin/comments/delete/user/<int:user_id>")
@login_required
@roles_required(["Admin", "Superadmin"])
def delete_all_comments_by_user(user_id):
    try:
        user = User.query.filter_by(id=user_id).first_or_404()
        num_deleted = Comment.query.filter_by(user_id=user_id).delete()

        if num_deleted > 0:
            db.session.commit()
            flash(f"Deleted {num_deleted} comments by {user.username}.", "success")
        else:
            flash(f"No comments by {user.username} to delete.", "info")

    except Exception as e:
        flash("An error occurred while deleting comments.", "error")
        db.session.rollback()
        abort(500)

    # Redirect back to the user details page
    return redirect(url_for("users.user_details", user_id=user_id))


# Method that returns total number of comments
@comments.route("/api/comments/number_of_comments", methods=["GET"])
def number_of_comments():
    number_of_comments = Comment.query.count()
    return jsonify(number_of_comments=number_of_comments)


@comments.route("/api/comments/count_by_months", methods=["GET"])
def comment_count():
    commentCountList = []

    for x in range(1, 13):
        commentCountList.append(get_comments_count(x))

    return jsonify(commentCountList=commentCountList)


def get_comments_count(month):
    current_year = datetime.utcnow().year
    start_date = datetime(current_year, month, 1)
    if month == 12:
        end_date = datetime(current_year + 1, 1, 1)
    else:
        end_date = datetime(current_year, month + 1, 1)

    comment_count = Comment.query.filter(
        Comment.date_posted >= start_date, Comment.date_posted < end_date
    ).count()

    # response = {"month": month, "year": current_year, "comment_count": comment_count}
    # return jsonify(response)
    return comment_count
