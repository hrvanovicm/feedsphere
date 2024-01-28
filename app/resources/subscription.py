import falcon
from sqlalchemy import Column, Integer, String, DateTime, func

from app.database import Base
from app.resources import BaseResource


def validate_create(req, res, resource, params):
    # schema = {}
    #
    # v = Validator(schema)
    #
    # if not v.validate(req.media):
    #     raise Exception("Invalid parameters")

    # TODO: Implement schema for creating subscription object
    pass


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def as_dict(self):
        return {'id': self.id, 'name': self.name, 'url': self.url}


class SubscriptionResource(BaseResource):
    def on_get(self, req, resp):
        session = req.context['session']
        query = session.query(Subscription).all()
        data = [sub.as_dict() for sub in query]
        self.handle_success(resp, data)

    @falcon.before(validate_create)
    def on_post(self, req, resp):
        session = req.context['session']

        sub = Subscription(
            name=req.media['name'],
            url=req.media['url']
        )

        # TODO: implement unique handler

        session.add(sub)
        session.commit()
        data = sub.as_dict()
        self.handle_success(resp, data)

    def on_get_subscription(self, req, resp, subscription_id):
        session = req.context['session']

        query = session.query(Subscription).get(subscription_id)

        if query is None:
            self.handle_not_found(resp)
            return

        data = query.as_dict()
        self.handle_success(resp, data)

    def on_delete_subscription(self, req, resp, subscription_id):
        raise NotImplemented("realllly dude")
