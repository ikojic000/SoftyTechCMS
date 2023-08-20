from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    SubmitField,
    TextAreaField,
    FileField,
    SelectField,
)
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

from flaskblog.models import Category


# ADMIN SIDE FORMS
# Form for adding posts
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=5, max=30)])
    subtitle = StringField(
        "Subitle", validators=[DataRequired(), Length(min=5, max=30)]
    )
    description = TextAreaField(
        "Description", validators=[DataRequired(), Length(min=5, max=100)]
    )
    slug = StringField("Slug", validators=[DataRequired(), Length(min=5, max=30)])
    headImg = FileField("Post Header Image", validators=[FileAllowed(["jpg", "png"])])
    category = SelectField(
        "Category",
        coerce=int,  # Ensure that the selected value is stored as an integer (category_id)
        choices=[(category.id, category.name) for category in Category.query.all()],
    )
    language = SelectField(
        "Language", choices=[("HRV", "Hrvatski"), ("ENG", "English")]
    )
    author = StringField(
        "Author",
        validators=[DataRequired(), Length(min=5, max=15)],
    )
    content = TextAreaField("Content")
    isPublished = BooleanField("Published")
    submit = SubmitField("Save")
