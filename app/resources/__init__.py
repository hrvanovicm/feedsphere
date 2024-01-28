import json
import falcon

class BaseResource:
    def handle_success(self, resp, data):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        resp.body = json.dumps(data)

    def handle_not_found(self, resp):
        resp.status = falcon.HTTP_404
        resp.body = json.dumps({'err': 'Not found'})

    def _decode_body(self, req):
        return req.body

from . import *