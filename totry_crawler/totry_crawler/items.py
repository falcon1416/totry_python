# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TotryCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Item(scrapy.Item):
    menuID = scrapy.Field()
    proejctName = scrapy.Field()
    deptName = scrapy.Field()
    areaName = scrapy.Field()
    seTime = scrapy.Field()
    overView = scrapy.Field()
    supportFrom = scrapy.Field()

    materials= scrapy.Field()
    support= scrapy.Field()
    system= scrapy.Field()
    source= scrapy.Field()
    condition=scrapy.Field()
    estate=scrapy.Field()