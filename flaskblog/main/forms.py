from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField, FileField, SelectField, SelectMultipleField, validators
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_wtf.file import FileAllowed




# Form for posting comments
class CommentForm(FlaskForm):
    comment = TextAreaField('Comment',
                        validators=[DataRequired(), Length(min=3, max=150)])
    submit = SubmitField('Comment')

# Form for search
class SearchForm(FlaskForm):
    search = StringField('Search',
                        validators=[DataRequired(), Length(min=3)])
    submit = SubmitField('')


# Form for contact page
class ContactForm(FlaskForm):
    name = StringField('Name',
                        validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    subject = StringField('Subject',
                        validators=[DataRequired(), Length(min=3, max=20)])
    message = TextAreaField('Message',
                        validators=[DataRequired(), Length(min=5, max=50)])
    submit = SubmitField('Send')
