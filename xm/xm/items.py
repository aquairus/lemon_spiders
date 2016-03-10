# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class xmItem(scrapy.Item):

    name=scrapy.Field()
    username=scrapy.Field()
    count=scrapy.Field()
    category=scrapy.Field()
    tag_list=scrapy.Field()
    album_list=scrapy.Field()
    url=scrapy.Field()
