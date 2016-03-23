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
space_re = re.compile(r"\s+")

class ar11Spider(CrawlSpider):
    name = "ar11"
    allowed_domains = ["www.elkhabar.com"]
    start_urls = ["http://www.elkhabar.com"]

    rules=(
    Rule(LinkExtractor(allow=('/\d{6}'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_news'),\

    Rule(LinkExtractor(allow=('category|news|page'),deny=('program|feed|cartoon|vedio|podcast|adv|about|error|ablum')),
                follow=True,callback='parse_url'),


    # Rule(LinkExtractor(allow=('.'),deny=('\d{7}|video|feed')),
    #             follow=False),
    )
    def parse_url(self, response):
        #print response.url
        pass
    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.xpath("//h4/text()").extract()[0].strip()
            contents=response.xpath("//div[@id='body_content']").extract()[0].strip()
        except BaseException,e:
            print e
            print url
            return
        contents=space_re.sub(" ",contents)
        times=response.css('p[style*=direction] span span').extract()#("//p[@style='direction:rtl;']/text()").extract()[0]
        time=times[1][27:-7]+" "+times[3][27:-7]
        # print time[1][27:-7]
        # print time[3][27:-7]
        #time=time[54:-12]
        # time=""
        ar=arItem()
        ar["title"]=title
        ar["content"]=contents
        ar["review"]=""
        ar["time"]=time
        ar["url"]=url
        return ar
