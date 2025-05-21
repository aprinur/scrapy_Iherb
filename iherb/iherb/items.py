# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class IherbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Name = scrapy.Field()
    URL = scrapy.Field()
    Brand = scrapy.Field()
    Stars = scrapy.Field()
    Reviews = scrapy.Field()
    Image_url = scrapy.Field()
    Flavours = scrapy.Field()
    Packages_Quantity_and_Price = scrapy.Field()
    Authentic_level = scrapy.Field()
    Best_by = scrapy.Field()
    First_available = scrapy.Field()
    Shipping_weight = scrapy.Field()
    Product_code = scrapy.Field()
    UPC = scrapy.Field()
    Dimension = scrapy.Field()


class IherbAlchemy(Base):
    __tablename__ = 'Iherb_Product_Information'

    id = Column(Integer, nullable=False, primary_key=True, unique=True)
    Name = Column(String, nullable=False)
    URL = Column(String, nullable=False)
    Brand = Column(String, nullable=False)
    Stars = Column(Float, nullable=True)
    Reviews = Column(Integer, nullable=True)
    Image_url = Column(String, nullable=True)
    Flavours = Column(String, nullable=True)
    Packages_Quantity_and_Price = Column(String, nullable=True)
    Authentic_level = Column(String, nullable=False)
    Best_by = Column(String, nullable=True)
    First_available = Column(String, nullable=True)
    Shipping_weight = Column(String, nullable=False)
    Product_code = Column(String, nullable=True)
    UPC = Column(Integer, nullable=True)
    Dimension = Column(String, nullable=False)


db_path = 'sqlite:///iherb.db'
engine = create_engine(db_path)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
