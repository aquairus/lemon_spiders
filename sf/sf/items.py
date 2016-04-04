# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class sfItem(scrapy.Item):

    title=scrapy.Field()
    bid=scrapy.Field()
    publish=scrapy.Field()
    update=scrapy.Field()
    remote=scrapy.Field()
    local=scrapy.Field()
    vulner=scrapy.Field()
    dis=scrapy.Field()

class disItem(scrapy.Item):
    bid=scrapy.Field()
    dis=scrapy.Field()

class expItem(scrapy.Item):
    bid=scrapy.Field()
    exp=scrapy.Field()
