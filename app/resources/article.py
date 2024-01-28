from sqlalchemy import Column, Integer, String, DateTime, func

from app.database import Base
from app.resources import BaseResource


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False)
    short_desc = Column(String, unique=True, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

    def as_dict(self):
        return {'id': self.id, 'title': self.title}


class ArticleResource(BaseResource):
    def on_get(self, req, resp):
        session = req.context["session"]
        query = session.query(Article).all()
        data = [sub.as_dict() for sub in query]
        self.handle_success(resp, data)
