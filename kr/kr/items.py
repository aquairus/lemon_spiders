# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy





class cptItem(scrapy.Item):
    title=scrapy.Field()
    novelId=scrapy.Field()
    volumeNo=scrapy.Field()
    review=scrapy.Field()

class krItem(scrapy.Item):
    content=scrapy.Field()
    review=scrapy.Field()
