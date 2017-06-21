# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class ProxyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class yItem(scrapy.Item):
    biz_name = Field()
    url = Field()
    star = Field()
    number_of_reviews = Field()
    dollar = Field()
    category = Field()
    address = Field()
    neighborhood_str_list = Field()
    address = Field()
    biz_phone = Field()
