import datetime
import jwt
from flask import current_app

def create_token(user_id, refresh=False):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=current_app.config["TOKEN_EXPIRY"]),
        'iat': datetime.datetime.utcnow(),
        'sub': f"{user_id}_refresh" if refresh else user_id
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm='HS256')
