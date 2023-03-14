from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up database connection
engine = create_engine("sqlite:///data/aco.db", echo=True)

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a Base class for declarative models
Base = declarative_base()


# class SessionManager(object):
#     def __init__(self):
#         self.session = Session()
def SessionManager():
    return Session()
