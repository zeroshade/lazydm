"""SQLAlchemy Metadata and Session object"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from pytz import timezone

__all__ = ['Base', 'Session']

# SQLAlchemy session manager. Updated by model.init_model()
Session = scoped_session(sessionmaker())

# The declarative Base
Base = declarative_base()

metadata = Base.metadata

def defdate():
    return datetime.now(timezone("America/New_York"))
