# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonscrapingItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    price_discount = scrapy.Field()
    price_discount_percent = scrapy.Field()
    screenshot_filename = scrapy.Field()
