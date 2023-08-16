from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


# Form for posting comments
class CommentForm(FlaskForm):
    comment = TextAreaField(
        "Comment", validators=[DataRequired(), Length(min=3, max=150)]
    )
    submit = SubmitField("Comment")
