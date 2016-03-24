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

class ar16Spider(CrawlSpider):
    name = "ar16"
    allowed_domains = ["champress.net"]
    start_urls = ["http://www.champress.net"]

    rules=(
    Rule(LinkExtractor(allow=('Article'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_news'),\

    )


    def parse_start_url(self,response):
        pre_url="http://www.champress.net/index.php?q=ar/Article/view/"
        for id in xrange(9905,67613):
            url=pre_url+str(id)
            sleep(0.01)
            yield Request(url,callback=self.parse_news)

    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.css("h1[class*=Article]::text").extract()[0].strip()
            times=response.css('div[id*=mainContent] div::text').extract()
            contents=response.css("div[id*=mainContent]").extract()[0]
            #contents=response.xpath("div[@class='mainContent']").extract()[0]

        except BaseException,e:
            print e
            return

        for t in times:
            if date_re.search(t):
                time=t

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
