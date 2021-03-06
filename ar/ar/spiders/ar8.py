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
tag_re = re.compile(r"\\t+|<h4.*?>|<h3.*?>|</h3>|<div.*?>|<section.*?>|</section>|</article>")
space_re = re.compile(r"\s+")

class ar8Spider(CrawlSpider):
    name = "ar8"
    allowed_domains = ["almotamar.net"]
    start_urls = ["http://www.almotamar.net/news/"]

    rules=(
    Rule(LinkExtractor(allow=('news/\d+.htm'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_news'),\

    )


    def parse_start_url(self,response):
        pre_url="http://www.almotamar.net/news/"
        for id in xrange(2024,129242):
            url=pre_url+str(id)+".htm"
            sleep(0.01)
            yield Request(url,callback=self.parse_news)

    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.css("a[class*=title]::text").extract()[0].strip()
            time=response.css('div[class*=comments]::text').extract()[0].strip()
            contents=response.css('div[class=news]').extract()[0].strip()

        except BaseException,e:
            print e
            print url
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
