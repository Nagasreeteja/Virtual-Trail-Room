#imports for DATABASE
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()

#User table details
class User(Base):
    __tablename__ = 'user'

    user_name = Column(String(200), nullable = False)
    email = Column(String(250), primary_key = True)
    password = Column(String(250))

#Category table details
class Category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key = True)
    category_name = Column(String(250), nullable = False)

    #Serializing category object
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'category_id' : self.category_id,
           'category_name' : self.category_name,
       }

#Item table details
class Item(Base):
    __tablename__ = 'items'

    item_id = Column(Integer, primary_key = True)
    item_name = Column(String(200), nullable = False)
    item_count = Column(Integer, default = 0)
    price = Column(Integer, nullable = False)
    picture = Column(String(2000), nullable = False)
    created_time = Column(DateTime, default = datetime.now())
    category_id = Column(Integer, ForeignKey('category.category_id'))
    category = relationship(Category)
    user_email = Column(Integer, ForeignKey('user.email'))
    user = relationship(User)

    #Serializing item object
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'item_id' : self.item_id,
            'item_name' : self.item_name,
            'item_count' : self.item_count,
            'price' : self.price,
            'picture' : self.picture,
            'description' : self.description,
            'created_time' : self.created_time,
            'category_id' : self.category_id
        }

class Cart(Base):
    __tablename__ = 'cart'

    item_id = Column(Integer, ForeignKey('items.item_id'), primary_key = True)
    item = relationship(Item)
    item_quantity = Column(Integer, default = 1)
    email = Column(Integer, ForeignKey('user.email'))
    user = relationship(User)

    #Serializing item object
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'item_id' : self.item_id,
            'item_quantity' : self.item_quantity,
            'category_id' : self.category_id
        }

engine = create_engine('sqlite:///shoppingsite.db')

Base.metadata.create_all(engine)
