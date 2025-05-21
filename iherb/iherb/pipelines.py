# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging

# useful for handling different item types with a single interface
from sqlalchemy.exc import IntegrityError

from db_exporter import db_toexcel
from .items import Session, IherbAlchemy


class IherbPipeline:
    def process_item(self, item, spider):
        item['Flavours'] = ', '.join(item['Flavours']) if item['Flavours'] else item['Flavours']

        if isinstance(item['Packages_Quantity_and_Price'], list):
            item['Packages_Quantity_and_Price'] = ', '.join(item['Packages_Quantity_and_Price'])
        elif item['Packages_Quantity_and_Price']:
            item['Packages_Quantity_and_Price'] = item['Packages_Quantity_and_Price'].strip()
        else:
            item['Packages_Quantity_and_Price'] = None

        item['Stars'] = float(item['Stars']) if item['Stars'] else item['Stars']
        item['Reviews'] = int(item['Reviews'].replace(',', '')) if item['Reviews'] else item['Reviews']
        item['UPC'] = int(item['UPC'])
        item['Best_by'] = item['Best_by'].strip().removeprefix("Best by: ") if item['Best_by'] else item['Best_by']
        item['First_available'] = item['First_available'].strip() if item['First_available'] else item[
            'First_available']
        item['Dimension'] = item['Dimension'].strip() if item['Dimension'] else item['Dimension']
        return item


class AlchemyPipeline:
    def __init__(self):
        pass


    def open_spider(self, spider):
        self.session = Session()


    def close_spider(self, spider):
        self.session.close()
        db_toexcel()


    def process_item(self, item, spider):
        product = IherbAlchemy(**item)

        try:
            self.session.add(product)
            self.session.commit()
            print(f'Product {product.Name} added')
        except IntegrityError:
            self.session.rollback()
            print(f'Skipping duplicate: {product.Name}')
        except Exception as e:
            self.session.rollback()
            logging.warning(f'Skipping item {product.Name} due to error: {e}')

        return item
