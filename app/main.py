import sys
from wsgiref.simple_server import make_server

import falcon
from apscheduler.schedulers.background import BackgroundScheduler

from app.config import PORT, HOST
from app.database import Session
from app.jobs.fetch_articles import fetch_articles
from app.jobs.setup import run_setup
from app.middleware.authenticator import Authenticator
from app.middleware.db_session_manager import DBSessionManager
from app.resources import subscription, article, actuator, user

middleware = [DBSessionManager(Session), Authenticator()]
app = falcon.App(middleware=middleware)

if __name__ == "__main__":
    if '--setup' in sys.argv:
        run_setup()

    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_articles, 'interval', hours=1)
    scheduler.start()

    app.add_route("/actuator", actuator.ActuatorResource())
    app.add_route("/subscriptions", subscription.SubscriptionResource())
    app.add_route("/subscriptions/{subscription_id}", subscription.SubscriptionResource(), suffix="subscription")
    app.add_route("/articles", article.ArticleResource())
    app.add_route("/users", user.UserResource())
    app.add_route("/users/{user_id}", user.UserResource(), suffix="user")

    with make_server(HOST, int(PORT), app) as httpd:
        print("Serving at {}:{}".format(HOST, PORT))
        httpd.serve_forever()
