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
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from SoftyTechCMS.models import Category
from SoftyTechCMS.posts.utils import validate_slug, validate_subtitle, validate_title


class PostForm(FlaskForm):
    """
    Form for adding posts.

    Attributes:
        title (StringField): The title of the post.
        subtitle (StringField): The subtitle of the post.
        description (TextAreaField): A description of the post.
        slug (StringField): A unique slug for the post's URL.
        headImg (FileField): An image to be used as the post's header image.
        category (QuerySelectField): The category to which the post belongs.
        language (SelectField): The language of the post.
        author (StringField): The author of the post.
        content (TextAreaField): The main content of the post.
        isPublished (BooleanField): Whether the post is published or in draft.
        submit (SubmitField): The submission button for saving the post.
    """

    title = StringField(
        "Title",
        validators=[
            DataRequired(message="Title is required."),
            Length(
                min=5,
                max=100,
                message="Title must be between 5 and 100 characters long!",
            ),
            # validate_title,
        ],
    )
    subtitle = StringField(
        "Subitle",
        validators=[
            DataRequired(message="Subtitle is required."),
            Length(
                min=5,
                max=100,
                message="Subtitle must be between 5 and 100 characters long!",
            ),
            # validate_subtitle,
        ],
    )
    description = TextAreaField(
        "Description",
        validators=[
            DataRequired(message="Description is required."),
            Length(
                min=5,
                max=350,
                message="Description must be between 5 and 350 characters long!",
            ),
        ],
    )
    slug = StringField(
        "Slug",
        validators=[
            DataRequired(message="Slug is required."),
            Length(
                min=3,
                max=100,
                message="Slug must be between 3 and 100 characters long!",
            ),
            # validate_slug,
        ],
    )
    headImg = FileField(
        "Post Header Image",
        validators=[
            FileAllowed(
                ["jpg", "jpeg"],
                message="Only .jpg, and .jpeg files are allowed!",
            )
        ],
    )
    category = QuerySelectField(
        "Category",
        query_factory=lambda: Category.query,
        allow_blank=True,
        get_label="name",
        validators=[DataRequired(message="Category is required.")],
    )
    language = SelectField(
        "Language", choices=[("HRV", "Hrvatski"), ("ENG", "English")]
    )
    author = StringField(
        "Author",
        validators=[
            DataRequired(message="Author is required."),
            Length(
                min=5,
                max=15,
                message="Author must be between 5 and 15 characters long!",
            ),
        ],
    )
    content = TextAreaField("Content")
    isPublished = BooleanField("Published")
    submit = SubmitField("Save")
