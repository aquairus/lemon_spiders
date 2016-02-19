# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class qItem(scrapy.Item):
    # define the fields for your item here like:
    content=scrapy.Field()
    review = scrapy.Field()
    qid= scrapy.Field()



class aItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    review = scrapy.Field()
    qid= scrapy.Field()
    pid= scrapy.Field()
