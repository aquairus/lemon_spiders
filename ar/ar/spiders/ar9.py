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

class ar9Spider(CrawlSpider):
    name = "ar9"
    allowed_domains = ["wattan.tv"]
    start_urls = ["http://www.wattan.tv",]

    rules=(
    Rule(LinkExtractor(allow=('/\d{3,6}.html'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_news'),\
    Rule(LinkExtractor(allow=('24|news|page'),deny=('program|feed|cartoon|vedio|podcast|adv|about|error|\d{5,6}')),
                follow=True),

              )
    # Rule(LinkExtractor(allow=('.'),deny=('\d{3,6}')),
    #             follow=False,callback='parse_url'),
    #
    #         #  )
    def parse_url(self, response):
        print response.url
        #pass
    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.xpath("//h1/text()").extract()[0]
            contents=response.xpath("//div[@class='page-content']").extract()[0]
        except BaseException,e:
            print e
            print url
            return
        #
        time=response.xpath("//div[@class='page-date']/text()").extract()[0].strip()
        # # #print title
        # # content=""
        # # for c in contents:
        # #     content=content+c
        # #
        ar=arItem()
        ar["title"]=title
        ar["content"]=contents
        ar["review"]=""
        ar["time"]=time
        ar["url"]=url
        return ar
