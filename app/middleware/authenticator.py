import base64

import bcrypt
import falcon
from falcon import Request

from app.resources.user import User


class Authenticator:
    def __init__(self):
        pass

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def process_request(self, req: Request, resp, resource=None):
        token = req.get_header('Authorization')

        if token is None:
            raise falcon.HTTPUnauthorized(description='Authentication required')

        decoded_token = base64.b64decode(token).decode('utf-8')
        username, password = decoded_token.split(':', 1)

        session = req.context['session']

        user = session.query(User).filter_by(username=username).first()

        password_valid = False

        if user is not None:
            password_valid = bcrypt.checkpw(password.encode('utf-8'), user.password)

        if user is None or password_valid is False:
            raise falcon.HTTPUnauthorized(description='Authentication required')

        req.context['user'] = user

    def process_response(self, req, resp, resource=None, req_succeeded=True):
        pass
