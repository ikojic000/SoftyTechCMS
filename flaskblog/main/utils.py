from flaskblog import mail
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
    # Create a Message object with the specified subject, sender, and recipients
    message = Message(
        subject,
        sender="softythetechguy@gmail.com",
        recipients=["softythetechguy@gmail.com"],
    )

    message.body = f"""
    From: {name} <{email}>
    {email_message}
    """

    # Send the email
    mail.send(message)
