# noinspection PyUnresolvedReferences
import json

# noinspection PyUnresolvedReferences
import falcon

from . import *


# noinspection PyMethodMayBeStatic
class BaseResource:
    def handle_success(self, resp, data=None, code=falcon.HTTP_200):
        resp.status = code
        resp.content_type = falcon.MEDIA_JSON

        if data is not None:
            resp.media = data

    def handle_not_found(self, resp):
        resp.status = falcon.HTTP_404
        resp.media = {
            'error': 'Resource not found!'
        }

    def handle_validation_failed(self, resp):
        resp.status = falcon.HTTP_400
        resp.media = {
            'title': 'Something went wrong!'
        }
