from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField, FileField, SelectField, SelectMultipleField, validators
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_wtf.file import FileAllowed


# ADMIN SIDE FORMS
# Form for adding posts
class PostForm(FlaskForm):
    title = StringField('Title', 
        	            validators=[DataRequired(), Length(min=5, max=30)])
    subtitle = StringField('Subitle', 
                        validators=[DataRequired(), Length(min=5, max=30)])
    description = TextAreaField('Description', 
                        validators=[DataRequired(), Length(min=5, max=100)])
    slug = StringField('Slug', 
                        validators=[DataRequired(), Length(min=5, max=30)])
    headImg = FileField('Post Header Image', validators=[FileAllowed(['jpg', 'png'])])
    category = SelectField('Category', 
                        choices=[('News', 'News'), ('Reviews', 'Reviews'), ('Commentary', 'Commentary')]) 
    language = SelectField('Language', 
                        choices=[('HRV', 'Hrvatski'), ('ENG', 'English')])
    author = StringField('Author', 
                        validators=[DataRequired(), Length(min=5, max=15)])
    content = TextAreaField('Content')
    submit = SubmitField('Post')

# Form for uploading images to a folder on a server
class MediaForm(FlaskForm):
    mediaFile = FileField('Upload Media', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Upload')