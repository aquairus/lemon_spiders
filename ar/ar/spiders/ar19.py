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
tag_re = re.compile(r"\\t+|<h1.*?>|</h1>|<tr.*?>|</tr>|<tr>|<div.*?>|<table.*?>|</table>|</article>|</like>")
space_re = re.compile(r"\s+")
date_re = re.compile(r"\d+-\d+\d+")

class ar19Spider(CrawlSpider):
    name = "ar19"
    allowed_domains = ["almasdaronline.net"]
    start_urls = ["http://almasdaronline.net"]

    rules=(
    Rule(LinkExtractor(allow=('article/\d'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_news'),\

    )


    def parse_start_url(self,response):
        pre_url="http://almasdaronline.net/article/"
        for id in xrange(1006,80606):
            url=pre_url+str(id)
            sleep(0.01)
            yield Request(url,callback=self.parse_news)

    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.css("h1[id*=title]::text").extract()[0].strip()
            time=response.css('time[datetime]::text').extract()[0].strip()
            contents=response.css("div[class*=contents]").extract()[0]


        except BaseException,e:
            print e
            return


        contents=tag_re.sub(" ",contents)
        contents=space_re.sub(" ",contents)
        review=""

        ar=arItem()
        ar["title"]=title
        ar["content"]=contents
        ar["review"]=review
        ar["time"]=time
        ar["url"]=url
        return ar
