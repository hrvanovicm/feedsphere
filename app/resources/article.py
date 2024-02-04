from falcon import Request
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import relationship, lazyload

from app.database import Base
from app.resources import BaseResource
from app.resources.subscription import Subscription


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String, nullable=False)
    author_name = Column(String, nullable=True)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=True)
    published_at = Column(String, nullable=True)
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'))
    created_at = Column(DateTime, default=func.now())

    subscription = relationship(Subscription)

    def as_dict(self):
        return {
            'id': self.id,
            'link': self.link,
            'title': self.title,
            'author': {
                'name': self.author_name
            },
            'summary': self.summary,
            'published_at': self.published_at,
            'created_at': self.created_at.isoformat(),
            'subscription': self.subscription.as_dict()
        }


class ArticleResource(BaseResource):
    def on_get(self, req: Request, resp):
        session = req.context["session"]

        limit = req.get_param_as_int('limit', default=30)
        offset = req.get_param_as_int('offset', default=0)

        query = (session
                 .query(Article)
                 .options(lazyload(Article.subscription))
                 .limit(limit)
                 .offset(offset)
                 .all()
                 )
        data = [sub.as_dict() for sub in query]
        self.handle_success(resp, data)
