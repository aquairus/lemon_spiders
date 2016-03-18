# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class xmItem(scrapy.Item):


    ablum=scrapy.Field()
    author=scrapy.Field()

#    count_list=scrapy.Field()

    category_1=scrapy.Field()
    category_2=scrapy.Field()

    name_list=scrapy.Field()
    url_list=scrapy.Field()
    count_list=scrapy.Field()
    sount_cnt=scrapy.Field()

#    url=scrapy.Field()
