from app.resources import BaseResource
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
        self.handle_success(resp, data)
