"""Article Model"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime, UnicodeText
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from pytz import timezone
import pytz
from lazydm.model.meta import Base
from lazydm.model.comment import Comment

class Article(Base):
    __tablename__ = "lazydm_articles"

    id = Column(Integer, primary_key=True)
    author = Column(Unicode(50),nullable=False)
    pub_date = Column(DateTime(timezone=True),default=datetime.now(pytz.utc),index=True)
    mod_date = Column(DateTime(timezone=True),default=datetime.now(pytz.utc),onupdate=datetime.now(pytz.utc))
    title = Column(Unicode(50),nullable=False)
    slug = Column(Unicode(50),nullable=False,index=True,unique=True)
    content = Column(UnicodeText,nullable=False)

    comments = relationship(Comment, order_by=Comment.pub_date, backref="article")

#    def published(self):
#        date = pub_date

    def __unicode__(self):
	return self.title

    __str__ = __unicode__

