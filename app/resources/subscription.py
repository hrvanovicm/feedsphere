import re

import falcon
from cerberus import Validator
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.exc import IntegrityError

from app.database import Base
from app.resources import BaseResource
from app.resources.user import User


# I really do not have energy to write regex, so thanks gpt for this.
def url_validator(field, value, error):
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not url_pattern.match(value):
        error(field, "Invalid URL")


FIELDS = {
    "name": {"required": True, "minlength": 1, "maxlength": 32},
    "url": {
        "validator": url_validator,
        "required": True,
        "minlength": 11,
        "maxlength": 2083
    }
}


def validate_create(req, res, resource, params):
    schema = {
        "name": FIELDS["name"],
        "url": FIELDS["url"]
    }

    v = Validator(schema)

    if not v.validate(req.media):
        raise Exception(v.errors)


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

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
        user = req.context['user']

        sub = Subscription(
            name=req.media.get('name'),
            url=req.media.get('url'),
            user_id=user.id
        )

        try:
            session.add(sub)
            session.commit()
        except IntegrityError as ie:
            self.handle_validation_failed(resp)
            return

        data = sub.as_dict()
        self.handle_success(resp, data, falcon.HTTP_201)

    def on_get_subscription(self, req, resp, subscription_id):
        session = req.context['session']

        query = session.query(Subscription).get(subscription_id)

        if query is None:
            self.handle_not_found(resp)
            return

        data = query.as_dict()
        self.handle_success(resp, data)

    def on_put_subscription(self, req, resp, subscription_id):
        session = req.context['session']

        query = session.query(Subscription).get(subscription_id)

        if query is None:
            self.handle_not_found(resp)
            return

        if req.media.get('name') is not None:
            query.name = req.media.get('name')

        if req.media.get('url') is not None:
            query.url = req.media.get('url')

        data = query.as_dict()
        self.handle_success(resp, data)

    def on_delete_subscription(self, req, resp, subscription_id):
        session = req.context['session']

        query = session.query(Subscription).get(subscription_id)

        if query is None:
            self.handle_not_found(resp)
            return

        try:
            session.delete(query)
            session.commit()
        except IntegrityError:
            self.handle_validation_failed(resp)

        self.handle_success(resp, None, falcon.HTTP_204)
