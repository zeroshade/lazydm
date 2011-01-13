"""The application's model objects"""
from lazydm.model.meta import Session, Base

import logging

log = logging.getLogger(__name__)

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)


