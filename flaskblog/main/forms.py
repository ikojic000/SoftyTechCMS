from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, Length


# Form for search
class SearchForm(FlaskForm):
    """
    Search form for user queries.

    Attributes:
        search (StringField): Text field for entering search queries.
        submit (SubmitField): Submit button for executing the search.
    """

    search = StringField("Search", validators=[DataRequired(), Length(min=3)])
    submit = SubmitField("")


# Form for contact page
class ContactForm(FlaskForm):
    """
    Contact form for users to send messages.

    Attributes:
        name (StringField): Text field for entering the sender's name.
        email (StringField): Text field for entering the sender's email address.
        subject (StringField): Text field for entering the message subject.
        message (TextAreaField): Text area for entering the message content.
        submit (SubmitField): Submit button for sending the message.
    """

    name = StringField(
        "Name",
        validators=[
            DataRequired(message="Name is required. Please enter your name."),
            Length(
                min=3, max=20, message="Name must be between 3 and 20 characters long!"
            ),
        ],
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    subject = StringField(
        "Subject",
        validators=[
            DataRequired(message="Subject is required."),
            Length(
                min=3,
                max=20,
                message="Subject must be between 3 and 20 characters long!",
            ),
        ],
    )
    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Message is required. Please enter your message."),
            Length(min=5, message="Message must be at least 5 characters long!"),
        ],
    )
    submit = SubmitField("Send")
