"""
SQL Alchemy Models for Repoze.what
"""
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime, UnicodeText, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import desc
from lazydm.model.meta import Base, metadata
import os
from hashlib import sha1

# This is the association table for the many-to-many relationship between
# groups and permissions.
group_permission_table = Table('lazydm_group_permission', metadata,
    Column('group_id', Integer, ForeignKey('lazydm_groups.id')),
    Column('permission_id', Integer, ForeignKey('lazydm_permissions.id')),
)

# This is the association table for the many-to-many relationship between
# groups and users
user_group_table = Table('lazydm_user_group', metadata,
    Column('user_id', Integer, ForeignKey('lazydm_users.id')),
    Column('group_id', Integer, ForeignKey('lazydm_groups.id')),
)

class Group(Base):
    __tablename__ = "lazydm_groups"
    
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255),nullable=False,index=True,unique=True)
    
    permissions = relationship('Permission', secondary=group_permission_table, backref='groups')
    users = relationship('User', secondary=user_group_table, backref='groups')
    
class Permission(Base):
    __tablename__ = "lazydm_permissions"
    
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255),nullable=False,index=True,unique=True)
    
class User(Base):
    __tablename__ = "lazydm_users"
    
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(100), unique=True, nullable=False)
    email = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(80), nullable=False)
    fullname = Column(Unicode(255), nullable=False)
    
    def _set_password(self, password):
        """Hash on the fly"""
        hashed_pass = password
        
        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password
        
        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(password_8bit + salt.hexdigest())
        hashed_pass = salt.hexdigest() + hash.hexdigest()
        
        # Make sure the end result is Unicode because SQLAlchemy wants
        # a unicode string
        if not isinstance(hashed_pass, unicode):
            hashed_pass = hashed_pass.decode('UTF-8')
        
        self.password = hashed_pass
        
    def _get_password(self):
        """ Return password hash """
        return self.password
    
    def validate_password(self, password):
        """ Check password input against existing credentials """
        hashed_pass = sha1()
        hashed_pass.update(password + self.password[:40])
        return self.password[40:] == hashed_pass.hexdigest()
        
