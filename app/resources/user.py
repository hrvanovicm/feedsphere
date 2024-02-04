import bcrypt
import falcon
from cerberus import Validator
from falcon import Request
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.exc import IntegrityError

from app.config import APP_KEY
from app.database import Base
from app.middleware import admin_privileges
from app.resources import BaseResource


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    def as_dict(self):
        return {'id': self.id, 'username': self.username, 'is_admin': self.is_admin}


FIELDS = {
    "username": {"required": True, "minlength": 3, "maxlength": 32},
    "password": {
        "required": True,
        "minlength": 8
    }
}


def validate_create(req, res, resource, params):
    schema = {
        "username": FIELDS["username"],
        "password": FIELDS["password"]
    }

    v = Validator(schema)

    if not v.validate(req.media):
        raise Exception(v.errors)


class UserResource(BaseResource):
    def on_get(self, req, resp):
        session = req.context['session']
        query = session.query(User).all()
        data = [sub.as_dict() for sub in query]
        self.handle_success(resp, data)

    @falcon.before(admin_privileges)
    @falcon.before(validate_create)
    def on_post(self, req, resp):
        session = req.context['session']

        user = User(
            username=req.media.get('username'),
            password=bcrypt.hashpw(req.media.get('password').encode('utf-8'), APP_KEY.encode('utf-8')),
            is_admin=req.media.get('is_admin', False)
        )

        try:
            session.add(user)
            session.commit()
        except IntegrityError as ie:
            self.handle_validation_failed(resp)
            return

        data = user.as_dict()
        self.handle_success(resp, data, falcon.HTTP_201)

    def on_get_user(self, req, resp, user_id):
        session = req.context['session']

        query = session.query(User).get(user_id)

        if query is None:
            self.handle_not_found(resp)
            return

        data = query.as_dict()
        self.handle_success(resp, data)

    @falcon.before(admin_privileges)
    def on_put_user(self, req, resp, user_id):
        session = req.context['session']

        query = session.query(User).get(user_id)

        if query is None:
            self.handle_not_found(resp)
            return

        if req.media.get('username') is not None:
            query.username = req.media.get('username')

        if req.media.get('password') is not None:
            query.password = bcrypt.hashpw(req.media.get('password').encode('utf-8'), APP_KEY.encode('utf-8'))

        data = query.as_dict()
        self.handle_success(resp, data)


    @falcon.before(admin_privileges)
    def on_delete_user(self, req, resp, user_id):
        session = req.context['session']

        query = session.query(User).get(user_id)

        if query is None:
            self.handle_not_found(resp)
            return

        try:
            session.delete(query)
            session.commit()
        except IntegrityError:
            self.handle_validation_failed(resp)

        self.handle_success(resp, None, falcon.HTTP_204)
