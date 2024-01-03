from app.api.v1 import BaseResource
from app.config import APP_NAME, APP_VERSION, MINIMAL_CLIENT_VERSION, CONFIG


class ActuatorResource(BaseResource):
    def on_get(self, req, resp):
        data = {
            'app': {
                'name': APP_NAME,
                'version': APP_VERSION,
            },
            'minimalClientVersion': MINIMAL_CLIENT_VERSION
        }
        self._on_success(resp, data)
