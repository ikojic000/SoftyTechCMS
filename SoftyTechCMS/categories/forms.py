from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


# Create a FlaskForm for adding categories
class CategoryForm(FlaskForm):
	"""
	Form for adding categories.

	Attributes:
		category (TextAreaField): The text area where users can enter the category name.
		submit (SubmitField): The submission button for adding a category.
	"""
	
	category = TextAreaField(
		"Category",
		validators=[
			DataRequired( ),  # Ensure that the category field is not empty
			Length(
				min=3,
				max=50,
				message="Category name must be between 3 and 50 characters long!",
			),  # Enforce a character length limit for category names
		],
	)
	submit = SubmitField(
		"Add Category"
	)  # Button for submitting the form to add a category
