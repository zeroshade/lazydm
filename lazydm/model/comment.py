from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime, UnicodeText, String
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from pytz import timezone
import pytz
from lazydm.model.meta import Base

class Comment(Base):
    __tablename__ = "lazydm_comments"

    id = Column(Integer, primary_key=True)
    type = Column(String(20),nullable=False)
    user = Column(Unicode(50),nullable=False)
    pub_date = Column(DateTime(timezone=True),default=datetime.now(timezone("America/New_York")),index=True)
    email = Column(Unicode(50),nullable=False)
    content = Column(UnicodeText,nullable=False)
    website = Column(Unicode(100),default=None)
    article_id = Column(Integer, ForeignKey('lazydm_articles.id', ondelete="CASCADE"))
    ip_addr = Column(String(20),nullable=False)

#    article = relationship(Article, backref=backref('comments', order_by=id))
