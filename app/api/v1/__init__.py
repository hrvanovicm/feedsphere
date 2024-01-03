import json
import falcon


class BaseResource:
    def _on_success(self, resp, data):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        resp.body = json.dumps(data)


from .actuator import ActuatorResource
