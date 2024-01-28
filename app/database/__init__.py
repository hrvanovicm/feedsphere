from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///storage/data/feedsphere.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()