from datetime import datetime

#from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
DB = SQLAlchemy()
Base = declarative_base()

# Model for user.
class User(Base):
    __tablename__ = 'account'

    id = Column(UUID(as_uuid=True), primary_key=True)
    username = relationship("Blog", back_populates="username")
    password = Column(String(200), nullable=False)


# Model for user's blog.
class Blog(Base):
    __tablename__ = 'blog'

    author_id = Column(Integer,
                ForeignKey("account.id"),
        primary_key=True, 
         index=True)
    title = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    username = relationship("User", back_populates="username")
    #author_id = Column(Integer, index=True)
    #email = Column(String(50), nullable=False)
    created = Column(DateTime, default=datetime.now())

class Search(DB.Model):
    __tablename__ = 'search'

    id = Column(UUID(as_uuid=True), primary_key=True)
    search_term = Column(Text, nullable=False)
    record = Column(Text, nullable=False)
    author_id = Column(Integer, index=True)