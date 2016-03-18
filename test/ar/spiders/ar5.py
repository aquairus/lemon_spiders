# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import arItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
time_re = re.compile(r"(\d+/)")

class ar5Spider(CrawlSpider):
    name = "ar5"
    allowed_domains = ["marebpress.net"]
    start_urls = ["http://marebpress.net",
    "http://marebpress.net/newsarchive.php"
         ]
#,follow=True
    rules=(Rule(LinkExtractor(allow=('sid=\d{6}'),deny=('helloworld|nfriend|print')) ,\
                follow=True,callback='parse_news'),\
             Rule(LinkExtractor(allow=('topic|page'),deny=('video|login|feed|image|article')),
                follow=True),
            #  Rule(LinkExtractor(allow=('.*'),deny=('video|help|login|news_details|rss|writer|image|article')),
            #   callback='parse_url'),


     )

    def parse_url(self, response):
        print response.url

    def parse_news(self, response):

        url=response.url
        try:
            pass
            title=response.xpath("//div[@class='news_title']/text()").extract()[0]
            contents=response.xpath("//div[@class='news_details']//p").extract()
        except BaseException,e:
            print e
            print url
            return

        time=response.xpath("//span[@class='news_date']/text()").extract()[0]
        #print title
        content=""
        for c in contents:
            content=content+c

        ar=arItem()
        ar["title"]=title
        ar["content"]=content
        ar["review"]=""
        ar["time"]=time
        ar["url"]=url
        return ar
