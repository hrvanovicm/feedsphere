from wsgiref.simple_server import make_server

import falcon

from app.config import PORT, HOST
from app.database import session
from app.middleware.db_session_manager import DBSessionManager
from app.resources import subscription, article, actuator

middleware = [DBSessionManager(session)]
app = falcon.App(middleware=middleware)

if __name__ == "__main__":
    app.add_route("/actuator", actuator.ActuatorResource())
    app.add_route("/subscriptions", subscription.SubscriptionResource())
    app.add_route("/subscriptions/{subscription_id}", subscription.SubscriptionResource(), suffix="subscription")
    app.add_route("/articles", article.ArticleResource())

    with make_server(HOST, int(PORT), app) as httpd:
        print("Serving at {}:{}".format(HOST, PORT))
        httpd.serve_forever()
