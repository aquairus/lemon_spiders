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
tag_re = re.compile(r"\\t+|<h4.*?>|<h3.*?>|</h3>|<div.*?>|<section.*?>|</section>|</article>")
space_re = re.compile(r"\s+")

class ar15Spider(CrawlSpider):
    name = "ar15"
    allowed_domains = ["echoroukonline.com"]
    start_urls = ["http://www.echoroukonline.com/ara/"]

    rules=(
    Rule(LinkExtractor(allow=('articles/\d'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_news'),\

    )


    def parse_start_url(self,response):
        pre_url="http://www.echoroukonline.com/ara/articles/"
        for id in xrange(1001,278095):
            url=pre_url+str(id)+".html"
            sleep(0.01)
            yield Request(url,callback=self.parse_news)

    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.css("div[class*=title] h3::text").extract()[0].strip()
            time=response.css('div[class*=meta] span::text').extract()[0].strip()
            contents=response.css('section[class*=contents]').extract()[0].strip()
            comments=response.css('article[class*=good] p::text').extract()
        except BaseException,e:
            print e
            return
        contents=tag_re.sub(" ",contents)
        contents=space_re.sub(" ",contents)
        review=""
        for com in comments:
            review=review+"<p>"+com+"</p>"

        ar=arItem()
        ar["title"]=title
        ar["content"]=contents
        ar["review"]=review
        ar["time"]=time
        ar["url"]=url
        return ar
