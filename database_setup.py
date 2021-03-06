from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(String(250), nullable=False, primary_key=True)
    username = Column(String(250))


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    category = Column(String(250), nullable=False)
    created_on = Column(Date, nullable=False)
    user = relationship(User)
    user_id = Column(String(250), ForeignKey('users.id'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'created_on': self.created_on
        }

engine = create_engine('sqlite:///itemcatalog.db')

Base.metadata.create_all(engine)
