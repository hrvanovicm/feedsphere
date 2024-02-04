from app.config import APP_NAME, APP_VERSION
from app.jobs.fetch_articles import fetch_articles
from app.resources import BaseResource


class ActuatorResource(BaseResource):
    # noinspection PyUnusedLocal
    def on_get(self, req, resp):
        data = {
            'app': {
                'name': APP_NAME,
                'version': APP_VERSION,
            }
        }
        self.handle_success(resp, data)
