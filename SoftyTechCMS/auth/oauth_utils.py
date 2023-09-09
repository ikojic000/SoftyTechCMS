import os

from flask import session

from SoftyTechCMS import oauth

# Google OAuth2 configuration
google = oauth.remote_app(
    "google",
    consumer_key=os.environ.get("GOOGLE_CLIENT_ID"),
    consumer_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    request_token_params={"scope": "email"},
    base_url="https://www.googleapis.com/oauth2/v1/",
    request_token_url=None,
    access_token_method="POST",
    access_token_url="https://accounts.google.com/o/oauth2/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
)

# Facebook OAuth2 configuration
facebook = oauth.remote_app(
    "facebook",
    consumer_key=os.environ.get("FACEBOOK_APP_ID"),
    consumer_secret=os.environ.get("FACEBOOK_APP_SECRET"),
    request_token_params={"scope": "email"},
    base_url="https://graph.facebook.com/",
    request_token_url=None,
    access_token_method="GET",
    access_token_url="/oauth/access_token",
    authorize_url="https://www.facebook.com/dialog/oauth",
)


# Token getter for Google OAuth
@google.tokengetter
def get_google_oauth_token():
    """
    Retrieve the Google OAuth2 access token from the session.

    Returns:
        tuple: A tuple containing the access token and an empty string.
    """
    return session.get("google_token")


# Token getter for Facebook OAuth
@facebook.tokengetter
def get_facebook_oauth_token():
    """
    Retrieve the Facebook OAuth2 access token from the session.

    Returns:
        tuple: A tuple containing the access token and an empty string.
    """
    return session.get("facebook_token")
