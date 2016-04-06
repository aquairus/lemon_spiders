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
tag_re = re.compile(r"\\t+|<h1.*?>|</h1>|<a.*?>|</a>|<ul.*?>|</ul>|<div.*?>|</div>|<li.*?>|</li>|<img.*?>|</like>|<strong>|</strong>|<iframe.*?/iframe>")
space_re = re.compile(r"\s+")
out_re = re.compile(r"<br>&amp.*?<br>|<br>http.*?<br>|<br>.*?&gt;<br>")

class ar31Spider(CrawlSpider):
    name = "ar31"
    allowed_domains = ["www.alyaum.com"]
    start_urls = ["http://www.alyaum.com"]

    rules=(
    Rule(LinkExtractor(allow=('article/\d+'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_news'),\

    )


    def parse_start_url(self,response):
        pre_url="http://www.alyaum.com/article/"
        for id in xrange(4009609,4129742):
            url=pre_url+str(id)
            sleep(0.2)
            yield Request(url,callback=self.parse_news)

    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.css("h2::text").extract()[0].strip()
            time=response.css('span[class=meta]::text').extract()[0].strip()
            #time=response.xpath("//*[@class='meta']").extract()[0]
            #time
            content=response.css("div[class=column9]").extract()[0]


        except BaseException,e:
            print e
            return


        content=tag_re.sub(" ",content)
        content=space_re.sub(" ",content)
        content=out_re.sub(" ",content)

        review=""

        ar=arItem()
        ar["title"]=title
        ar["content"]=content
        ar["review"]=review
        ar["time"]=time
        ar["url"]=url
        return ar
