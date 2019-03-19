from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///shoppingsite.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
user1 = User(user_name="Lalitha Garapati", email="lalithagarapati4859@gmail.com",
             password="Lalitha@4859")
session.add(user1)
session.commit()

user2 = User(user_name="K S L Supriya", email="supriyakommisetti111@gmail.com",
             password="Supriya")
session.add(user2)
session.commit()

# Items for Necklace
category = Category(category_name="Necklaces")
session.add(category)
session.commit()

item = Item(item_name = "White and Red Stone Combination Necklace", item_count = 30, price = "Rs.39999",
             picture = "/static/images/Necklace1/1.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "White Stoned Necklace with Centered Green Stone", item_count = 30, price = "Rs.33333",
             picture = "/static/images/Necklace1/2.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "Gucci Boule Sliver Necklace", item_count = 30, price = "Rs.17649",
             picture = "/static/images/Necklace1/3.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "Multi-shape Cross-over Necklace with White Stones", item_count = 30, price = "Rs.30149",
             picture = "/static/images/Necklace1/4.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "Gucci Boule Gold Color with White Stone Necklace", item_count = 30, price = "Rs.7649",
             picture = "/static/images/Necklace1/5.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "Carissa plunging design Necklace", item_count = 30, price = "Rs.23449",
             picture = "/static/images/Necklace1/6.png",
             category = category, user = user1)
session.add(item)
session.commit()


# Items for Ear Rings
category = Category(category_name="Ear Rings")
session.add(category)
session.commit()

item = Item(item_name = "Red Stoned Exquisite Blooming Earrings", item_count = 30, price = "Rs.569",
             picture = "/static/images/Earrings2/1.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "White Stoned Flower and Circle Earrings", item_count = 30, price = "Rs.700",
             picture = "/static/images/Earrings2/2.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "Blue Stoned Exquisite Blooming Hangings", item_count = 30, price = "Rs.569",
             picture = "/static/images/Earrings2/3.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "White Stone Delight Stud Earrings", item_count = 30, price = "Rs.440",
             picture = "/static/images/Earrings2/4.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "Antara Chandbali Gold Color Earrings", item_count = 30, price = "Rs.239",
             picture = "/static/images/Earrings2/5.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "White Stoned Chandelier Earrings", item_count = 30, price = "Rs.850",
             picture = "/static/images/Earrings2/6.png",
             category = category, user = user1)
session.add(item)
session.commit()


# Items for Tiaras
category = Category(category_name="Tiaras")
session.add(category)
session.commit()

item = Item(item_name = "Pink Flower with White Stars Tiara", item_count = 30, price = "Rs.125",
             picture = "/static/images/Tiaras3/1.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "Multi Colored Rose Flower Tiara", item_count = 30, price = "Rs.125",
             picture = "/static/images/Tiaras3/2.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "Multi Colored and Flowered Tiara", item_count = 30, price = "Rs.125",
             picture = "/static/images/Tiaras3/3.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "White Stoned Queen Tiara", item_count = 30, price = "Rs.525",
             picture = "/static/images/Tiaras3/4.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "Daisy Flowered White Tiara", item_count = 30, price = "Rs.125",
             picture = "/static/images/Tiaras3/5.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "Baby Pink Rose Flower Tiara", item_count = 30, price = "Rs.729",
             picture = "/static/images/Tiaras3/6.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "Shaded Rose Flower Combination Tiara", item_count = 30, price = "Rs.125",
             picture = "/static/images/Tiaras3/7.png",
             category = category, user = user1)
session.add(item)
session.commit()


# Items for Sun Glasses
category = Category(category_name="Glasses")
session.add(category)
session.commit()

item = Item(item_name = "Gray Shaded Oval Shaped Sun Glasses", item_count = 30, price = "Rs.400",
             picture = "/static/images/Sunglasses4/1.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "Black Framed Spectacles", item_count = 30, price = "Rs.300",
             picture = "/static/images/Sunglasses4/2.png",
             category = category, user = user1)
session.add(item)
session.commit()

item = Item(item_name = "Redish Pink Shaded Sun Glasses", item_count = 30, price = "Rs.500",
             picture = "/static/images/Sunglasses4/3.png",
             category = category, user = user1)
session.add(item)
session.commit()


# Items for Frocks
category = Category(category_name="Frocks")
session.add(category)
session.commit()

item = Item(item_name = "Red Short Frock with no Sleeves", item_count = 30, price = "Rs.700",
             picture = "/static/images/Frocks5/1.png",
             category = category, user = user2)
session.add(item)
session.commit()

item = Item(item_name = "Yellow Short Frock with Center Belt Sleeveless", item_count = 30, price = "Rs.900",
             picture = "/static/images/Frocks5/2.png",
             category = category, user = user2)
session.add(item)
session.commit()

item = Item(item_name = "Emoji pictured Sleeveless Frock", item_count = 30, price = "Rs.650",
             picture = "/static/images/Frocks5/3.png",
             category = category, user = user2)
session.add(item)
session.commit()

item = Item(item_name = "Floral Sleeveless Short Frock", item_count = 30, price = "Rs.690",
             picture = "/static/images/Frocks5/4.png",
             category = category, user = user2)
session.add(item)
session.commit()

item = Item(item_name = "Dark Blue Barbie Sleeveless Frock", item_count = 30, price = "Rs.500",
             picture = "/static/images/Frocks5/5.png",
             category = category, user = user2)
session.add(item)
session.commit()


# Items for Tops
category = Category(category_name="Tops")
session.add(category)
session.commit()

item = Item(item_name = "Violet Layered Short Top", item_count = 30, price = "Rs.749",
             picture = "/static/images/Tops6/1.png",
             category = category, user = user2)
session.add(item)
session.commit()

item = Item(item_name = "Baby Pink Short Top", item_count = 30, price = "Rs.499",
             picture = "/static/images/Tops6/2.png",
             category = category, user = user2)
session.add(item)
session.commit()

item = Item(item_name = "White Printed Tee Shirt for Girls", item_count = 30, price = "Rs.499",
             picture = "/static/images/Tops6/3.png",
             category = category, user = user2)
session.add(item)
session.commit()

item= Item(item_name = "White Tee with Violet Printing", item_count = 30, price = "Rs.499",
             picture = "/static/images/Tops6/4.png",
             category = category, user = user2)
session.add(item)
session.commit()

print("added menu items!")
