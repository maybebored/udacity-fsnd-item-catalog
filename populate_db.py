from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from database_setup import Product,Base

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy products
product1 = Product(title='Leather Bat', description='The perfect leather bat for whacking \'sixes\' right out of the ground.',
             category='Cricket', created_on = datetime.now())
session.add(product1)
session.commit()

product2 = Product(title='Leather Ball',description='The perfect leather ball for bowling those \'Googlys\'.',
             category='Cricket',created_on=datetime.now())
session.add(product2)
session.commit()

product3 = Product(title='Kneepad',description='The perfect knee pads for protecting against Bret Lee\'s pacers.',
             category='Cricket',created_on=datetime.now())
session.add(product3)
session.commit()

product4 = Product(title='Football Boots',description='Messi dreams about wearing these against his worst enemies.',
             category='Football',created_on=datetime.now())
session.add(product4)
session.commit()

product5 = Product(title='Supreme Football',description='It looks less than what it can do. Try kicking it.',
             category='Football',created_on=datetime.now())
session.add(product5)
session.commit()

product6 = Product(title='Silver Hockey Stick',description='India loves this so much they are trying hockey on ice now.',
             category='Ice Hockey',created_on=datetime.now())
session.add(product6)
session.commit()

product7 = Product(title='Heavy Metal Ball',description='Can\'t say more.',
             category='Putshot',created_on=datetime(2018,1,1))
session.add(product7)
session.commit()

print("Updated database");