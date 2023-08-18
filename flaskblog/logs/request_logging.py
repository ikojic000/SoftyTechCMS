from flask import g, request
from datetime import datetime
from flask_login import current_user
from flaskblog.models import RequestLog
from flaskblog import db


def before_request():
    g.start_time = datetime.utcnow()


def after_request(response):
    endpoint = request.endpoint
    method = request.method
    user_id = current_user.id if current_user.is_authenticated else None
    timestamp = g.start_time

    request_log = RequestLog(
        endpoint=endpoint, methodType=method, user_id=user_id, timestamp=timestamp
    )

    db.session.add(request_log)
    db.session.commit()

    return response
