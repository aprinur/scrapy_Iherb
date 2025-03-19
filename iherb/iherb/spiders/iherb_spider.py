import re
from typing import Any

import scrapy
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import IherbItem


class IherbSpiderSpider(CrawlSpider):
    name = "iherb_spider"
    allowed_domains = ["sg.iherb.com"]
    start_urls = ["https://sg.iherb.com/catalog/brandsaz"]
    # custom_settings = {
    #     'CLOSESPIDER_PAGECOUNT': 200
    # }

    denied_category = [r'^/c/supplements$', r'^/c/sports$', r'^/c/bath-personal-care$',
                       r'^/c/beauty$', r'^/c/grocery$', r'^/c/healthy-home$', r'^/c/baby-kids$',
                       r'^/c/pets$']

    brand_links = LinkExtractor(allow=r"^/c/[^/?]+$", deny=denied_category)
    pagination_links = LinkExtractor(allow=r"^/c/[^/?]+\?p=\d+$")
    products_links = LinkExtractor(allow=r"/pr/[^/]+\/\d+")

    rules = (
        Rule(brand_links, follow=True),
        Rule(pagination_links, follow=True),
        Rule(products_links, callback="parse_item"),
    )

    def parse_start_url(self, response: Response, **kwargs: Any) -> Any:
        for element in response.css('a[data-ga-event-action="Click Trending Brands"]::attr(href)'):
            yield scrapy.Request(element.get())

    def parse_item(self, response):
        pattern = r'\([^\(]+\)'
        for element in response.css('div[style*="flex-grow: 1"]'):
            product = IherbItem()
            product["Name"] = re.sub(pattern=pattern, repl='', string=element.css('h1#name ::text').get().strip())
            product['URL'] = response.url
            product["Brand"] = element.css('a[data-ga-event-label="Breadcrumb_Product-Brand-Link"] bdi::text').get()
            product["Stars"] = element.css('a.average-rating.scroll-to::text').get() or None
            product['Reviews'] = element.css('a.rating-count.scroll-to *::text').get() or None
            product["Image_url"] = element.css('div.thumbnail-item.selected img::attr(src)').get()
            product["Flavours"] = element.css('.thumbnail-tile::attr(title)').getall() or None
            if element.css('div.attribute-group-package-quantity.attribute-tile-group'):  # Multi-option with multiple prices
                options = [i.strip() for i in element.css('div.attribute-name::text').getall()]
                prices = [i.strip() for i in element.css('div.price-container bdi::text').getall()]
                product['Packages_Quantity_and_Price'] = " | ".join(str(i) for i in list(zip(options, prices)))
            elif response.css('section#super-special-price') and element.css('div.attribute-group-options.attribute-tile-group'):  # Multiple option with discount prices
                options = [elm.strip() for elm in element.css('div.attribute-name::text').getall()]
                special = element.css('a#special-price ::text').get()
                price = element.css('b.s24::text').get()
                product['Packages_Quantity_and_Price'] = f'{special}: {price} ({", ".join(options)})'
            elif element.css('div.attribute-group-options.attribute-tile-group'):  # Multi options with single price
                options = [i.strip() for i in response.css('div.attribute-name ::text').getall()]
                price = response.css('div.price-inner-text p::text').get().strip()
                product['Packages_Quantity_and_Price'] = " | ".join(str((option, price)) for option in options)
            elif element.css('a#special-price'):  # Single option with discount price
                special = response.css('a#special-price::text').get().strip()
                price = response.css('b.s24::text').get().strip()
                product['Packages_Quantity_and_Price'] = f'{special} {price}'
            elif response.css('span.title.title-prohibited'):  # Unavailable product in a region
                product['Packages_Quantity_and_Price'] = response.css('span.title.title-prohibited::text').get()
            else:  # Single option with single price
                option = element.css('span.package-quantity::text').get().strip() if element.css('span.package-quantity::text') else None
                price = response.css('div.price-inner-text p::text').get().strip()
                product['Packages_Quantity_and_Price'] = str((option, price))
            product["Authentic_level"] = element.css('li.color-primary::text').get().strip()
            spec = element.css('ul#product-specs-list')
            product["Best_by"] = spec.xpath(".//li[contains(., 'Best by:')]/text()").get() or None
            product["First_available"] = element.css('span.product-sale-date::text').get()
            product["Shipping_weight"] = element.css('span.product-shipping-weight-label::text').get().strip()
            product["Product_code"] = spec.xpath('.//li[contains(., "Product code:")]/span/text()').get()
            product["UPC"] = spec.xpath(".//li[contains(., 'UPC:')]/span/text()").get()
            product["Dimension"] = element.css('span#dimensions::text').get()

            yield product


'''
Re-arrange order of Package_Quantity_and_Pice based on actual page
'''
