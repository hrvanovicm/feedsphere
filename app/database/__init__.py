from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///storage/data/feedsphere.db')
Base.metadata.create_all(engine)
SessionMaker = sessionmaker(bind=engine)
Session = SessionMaker()

# noinspection PyUnresolvedReferences
from app.resources import subscription, article, actuator, user
