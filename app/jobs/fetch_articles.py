import feedparser
from bs4 import BeautifulSoup

from app.database import Session
from app.resources.article import Article
from app.resources.subscription import Subscription


def fetch_articles():
    session = Session
    subscriptions = session.query(Subscription).all()
    for subscription in subscriptions:
        feed = feedparser.parse(subscription.url)
        for entry in feed.entries:
            existing_article = session.query(Article).filter(Article.link == entry.link).first()
            if existing_article is not None:
                continue
            article = Article(
                author_name=entry.author,
                title=entry.title,
                summary=BeautifulSoup(entry.summary, 'html.parser').get_text(),
                link=entry.link,
                published_at=entry.published,
                subscription_id=subscription.id
            )
            session.add(article)
            session.commit()
