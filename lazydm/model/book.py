from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relationship
from lazydm.model.meta import Base
from sqlalchemy.ext.declarative import declared_attr

class Book(Base):
    __tablename__ = "lazydm_books"

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(100),nullable=False,unique=True,index=True)

    def __str__(self):
        return self.title

class BookData(object):
    @declared_attr
    def book_id(cls):
        return Column(Integer, ForeignKey('lazydm_books.id', ondelete='CASCADE'))
    
    @declared_attr
    def book(cls):
        return relationship("Book", lazy='joined')
