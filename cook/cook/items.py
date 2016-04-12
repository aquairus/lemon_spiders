# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class cookItem(scrapy.Item):

    title=scrapy.Field()
    ingredient=scrapy.Field()
    recipe=scrapy.Field()
    url=scrapy.Field()
