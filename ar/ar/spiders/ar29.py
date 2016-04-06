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
tag_re = re.compile(r"\\t+|<h1.*?>|</h1>|<a.*?>|</a>|<ul.*?>|</ul>|<div.*?>|</div>|<li.*?>|</li>|<span.*?>|</span>|<strong>|</strong>|<strong.*?>")
space_re = re.compile(r"\s+")
out_re = re.compile(r"<br>&amp.*?<br>|<br>http.*?<br>|<br>.*?&gt;<br>")

class ar29Spider(CrawlSpider):
    name = "ar29"
    allowed_domains = ["alrai.com"]
    start_urls = ["http://alrai.com"]

    rules=(
    Rule(LinkExtractor(allow=('article/\d+'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_news'),\

    )


    def parse_start_url(self,response):
        pre_url="http://alrai.com/article/"
        for id in xrange(11111,779138):
            url=pre_url+str(id)+".html"
            sleep(0.2)
            yield Request(url,callback=self.parse_news)

    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.css("h1::text").extract()[0].strip()
            time=response.css('div[class*=show] span::text').extract()[0].strip()
            contents=response.css("div[class*=content]").extract()[0]


        except BaseException,e:
            print e
            return


        contents=tag_re.sub(" ",contents)
        contents=space_re.sub(" ",contents)
        contents=out_re.sub(" ",contents)
        # content=""
        # for c in contents:
        #     #print c
        #     content=content+c
        #
        review=""
        ar=arItem()
        ar["title"]=title
        ar["content"]=contents
        ar["review"]=review
        ar["time"]=time
        ar["url"]=url
        return ar
