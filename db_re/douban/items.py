# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class topicItem(scrapy.Item):
    author=scrapy.Field()
    title=scrapy.Field()
    time=scrapy.Field()
    topic_content=scrapy.Field()
    answers=scrapy.Field()
    tid=scrapy.Field()
    total=scrapy.Field()

class ansItem(scrapy.Item):

    tid=scrapy.Field()
    pid=scrapy.Field()
    answers=scrapy.Field()





class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
