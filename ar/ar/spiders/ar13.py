# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import arItem
#from ajaxcrawl import driverSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from time import sleep
import re
from scrapy.http import Request


import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
space_re = re.compile(r"\s+")

class ar13Spider(CrawlSpider):
    name = "ar13"
    allowed_domains = ["www.bab.com"]
    start_urls = ["http://www.bab.com"]

    rules=(
    Rule(LinkExtractor(allow=('Node/\d{6}'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_news'),\

    )


    def parse_start_url(self,response):
        pre_url="http://www.bab.com/Node/"
        for id in xrange(100001,264650):
            url=pre_url+str(id)
            sleep(0.01)
            yield Request(url,callback=self.parse_news)

    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.xpath("//h3[@class='title-post']/text()").extract()[0].strip()
            contents=response.xpath("//div[@class='entry-content']").extract()[0].strip()
        except BaseException,e:
            print e
            print url
            return#'icon-calendar'
        contents=space_re.sub(" ",contents)

        time=response.css('p[class*=kp] span::text').extract()[1]#("//p[@style='direction:rtl;']/text()").extract()[0]

        ar=arItem()
        ar["title"]=title
        ar["content"]=contents
        ar["review"]=""
        ar["time"]=time
        ar["url"]=url
        return ar
