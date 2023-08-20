from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class CategoryForm(FlaskForm):
    category = TextAreaField(
        "Category", validators=[DataRequired(), Length(min=3, max=50)]
    )
    submit = SubmitField("Add Category")
