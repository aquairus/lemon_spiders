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
tag_re = re.compile(r"\\t+|<h1.*?>|</h1>|<tr.*?>|</tr>|<tr>|<div.*?>|<table.*?>|</table>|</article>")
space_re = re.compile(r"\s+")
date_re = re.compile(r"\d+-\d+\d+")

class ar20Spider(CrawlSpider):
    name = "ar20"
    allowed_domains = ["adenalgd.net"]
    start_urls = ["http://adenalgd.net"]

    rules=(
    Rule(LinkExtractor(allow=('news/\d'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_news'),\

    )


    def parse_start_url(self,response):
        pre_url="http://adenalgd.net/news/"
        for id in xrange(1024,198212):
            url=pre_url+str(id)
            sleep(0.01)
            yield Request(url,callback=self.parse_news)

    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.css("h1[id=mainTitle]::text").extract()[0].strip()
            time=response.css('span[class*=date]::text').extract()[0].strip()
            contents=response.css("div[id*=subjectfont] p").extract()
            #contents=response.xpath("div[@class='mainContent']").extract()[0]

        except BaseException,e:
            print e
            return

        content=""
        for p in contents:
            #print type(p)
            content=content+p

        content=tag_re.sub(" ",content)
        content=space_re.sub(" ",content)
        review=""

        ar=arItem()
        ar["title"]=title
        ar["content"]=content
        ar["review"]=review
        ar["time"]=time
        ar["url"]=url
        return ar
