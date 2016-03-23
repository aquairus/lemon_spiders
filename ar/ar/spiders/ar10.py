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

class ar10Spider(CrawlSpider):
    name = "ar10"
    allowed_domains = ["www.radioalgerie.dz"]
    start_urls = ["http://www.radioalgerie.dz"]

    rules=(
    Rule(LinkExtractor(allow=('/\d{8}/\d+.html'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_news'),\

    Rule(LinkExtractor(allow=('categories|news|page'),deny=('program|feed|cartoon|vedio|podcast|adv|about|error|ablum')),
                follow=True),


    # Rule(LinkExtractor(allow=('.'),deny=('\d{7}|video|feed')),
    #             follow=False),
    )
    def parse_url(self, response):
        print response.url
        #pass
    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.xpath("//h3[@class='title']/text()").extract()[0]
            contents=response.xpath("//div[@class='field-items']").extract()[2]
        except BaseException,e:
            print e
            print url
            return
        #time=""
        time=response.xpath("//div[@class='field-items']").extract()[0]
        time=time[54:-12]

        ar=arItem()
        ar["title"]=title
        ar["content"]=contents
        ar["review"]=""
        ar["time"]=time
        ar["url"]=url
        return ar
