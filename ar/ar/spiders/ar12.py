# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import arItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from time import sleep
import re
from scrapy.http import Request

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
space_re = re.compile(r"\s+|\\t|<div.*?>")

class ar12Spider(CrawlSpider):
    name = "ar12"
    allowed_domains = ["sarayanews.com"]
    start_urls = ["http://www.sarayanews.com"]

    rules=(
    Rule(LinkExtractor(allow=('/\d+/\d+/\d+/'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_news'),

    )


    def parse_start_url(self,response):
        pre_url="http://www.sarayanews.com/index.php?page=article&id="
        for id in xrange(186720,358725):
            url=pre_url+str(id)
            sleep(0.001)
            yield Request(url,callback=self.parse_news)

    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.xpath("//h2[@class='title']/text()").extract()[0].strip()
            contents=response.xpath("//div[@id='description']").extract()[0].strip()
        except BaseException,e:
            print e
            print url
            return

        times=response.css('p[class*=margthalf]::text').extract()[0]#("//p[@style='direction:rtl;']/text()").extract()[0]
        contents=space_re.sub("",contents)
        ar=arItem()
        ar["title"]=title
        ar["content"]=contents
        ar["review"]=""
        ar["time"]=times
        ar["url"]=url
        return ar
