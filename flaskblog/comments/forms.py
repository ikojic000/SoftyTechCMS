from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


# Form for posting comments
class CommentForm(FlaskForm):
    """
    Form for users to post comments.

    Attributes:
        comment (TextAreaField): The text area where users can enter their comment.
        submit (SubmitField): The submission button for posting comments.
    """

    comment = TextAreaField(
        "Comment",
        validators=[
            DataRequired(
                message="Please enter a comment."
            ),  # Ensure comment is not empty
            Length(
                min=3,
                max=150,
                message="Comment must be between 3 and 150 characters long!",  # Enforce length limits
            ),
        ],
    )
    submit = SubmitField("Comment")  # Submission button for posting comments
