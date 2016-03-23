# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import arItem
#from ajaxcrawl import driverSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
time_re = re.compile(r"(\d+/)")

class ar8Spider(CrawlSpider):
    name = "ar8"
    allowed_domains = ["alwatanvoice.com"]
    start_urls = ["http://www.alwatanvoice.com",]

    rules=(
    Rule(LinkExtractor(allow=('/\d+/\d+/\d+/\d+'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_news'),\
    Rule(LinkExtractor(allow=('arabic|news|category|pulpit|\d{,4}.html$'),deny=('program|feed|cartoon|vedio|podcast|error')),
                follow=True,callback='parse_url'),

              )

    def parse_url(self, response):
        #print response.url
        pass
    def parse_news(self, response):

        url=response.url
        #print url
        try:
            pass
            title=response.xpath("//h1/text()").extract()[0]
            contents=response.xpath("//div[@id='fulltext']").extract()[0]
        except BaseException,e:
            print e
            print url
            return
        #
        time=response.xpath("//div[@class='publish-date']/text()").extract()[0].strip()
        # #print title
        # content=""
        # for c in contents:
        #     content=content+c
        #
        ar=arItem()
        ar["title"]=title
        ar["content"]=contents
        ar["review"]=""
        ar["time"]=time
        ar["url"]=url
        return ar
