import os
from SoftyTechCMS import mail
from flask import flash, abort
from flask_mail import Message


# Function to send an email
def send_mail(subject, name, email, email_message):
    """
    Send an email with the provided subject, sender, and content.

    Args:
        subject (str): The subject of the email.
        name (str): The name of the sender.
        email (str): The email address of the sender.
        email_message (str): The content of the email.

    Returns:
        None
    """
    try:
        # Create a Message object with the specified subject, sender, and recipients
        message = Message(
            subject,
            sender=os.environ.get("SoftyTechCMS_MAIL_USER"),
            recipients=[os.environ.get("SoftyTechCMS_MAIL_USER")],
        )

        message.body = f"""
        From: {name} <{email}>
        {email_message}
        """

        # Send the email
        mail.send(message)
    except Exception as e:
        print("error: ", e)
        flash("An error occurred while sending the email.", "error")
        abort(500, "An error occurred while sending the email. Please try again later.")
