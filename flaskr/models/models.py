from datetime import datetime

#from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from flaskr.database import Base

#Base = declarative_base()

#DB = SQLAlchemy()
# Model for user.
class User(Base):
    __tablename__ = 'account'

    id = Column(UUID(as_uuid=True), primary_key=True)
    username = relationship("Blog", back_populates="username")
    password = Column(String(200), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)

# Model for user's blog.
class Blog(Base):
    __tablename__ = 'blog'

    author_id = Column(Integer,
        primary_key=True, 
         index=True)
    title = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    username = relationship("User", back_populates="username")
    #author_id = Column(Integer, index=True)
    #email = Column(String(50), nullable=False)
    created = Column(DateTime, default=datetime.now())

    def __init__(self, username, author_id, title, created):
        self.username = username
        self.author_id = author_id
        self.title = title
        self.created = created

    def __repr__(self):
        return '<id {}>'.format(self.author_d)
