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

class ar14Spider(CrawlSpider):
    name = "ar14"
    allowed_domains = ["mobile.ammonnews.net"]
    start_urls = ["http://mobile.ammonnews.net"]

    rules=(
    Rule(LinkExtractor(allow=('articleno=\d'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_news'),\

    )


    def parse_start_url(self,response):
        pre_url="http://mobile.ammonnews.net/article.aspx?articleno="
        for id in xrange(30001,263319):
            url=pre_url+str(id)
            sleep(0.01)
            yield Request(url,callback=self.parse_news)

    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.xpath("//h3/text()").extract()[0].strip()
            time=response.css('div[class*=Date]::text').extract()[0].strip()[1:-1]
            contents=response.css('div[class*=Details] p').extract()[0].strip()

        except BaseException,e:
            print e
            return

        ar=arItem()
        ar["title"]=title
        ar["content"]=contents
        ar["review"]=""
        ar["time"]=time
        ar["url"]=url
        return ar
