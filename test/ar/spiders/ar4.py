# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import arItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
# import sys
# reload(sys)
# sys.setdefaultencoding( "utf-8" )

time_re = re.compile(r"(\d+/)")

class ar4Spider(CrawlSpider):
    name = "ar4"
    allowed_domains = ["alwatan.kuwait.tt"]
    start_urls = ["http://alwatan.kuwait.tt",
    "http://alwatan.kuwait.tt/mostviewed.aspx",
    "http://alwatan.kuwait.tt/writershomecolumn.aspx",
    "http://alwatan.kuwait.tt/categoryhome.aspx?catid=74",
    "http://alwatan.kuwait.tt/categoryhome.aspx?catid=40",
    "http://alwatan.kuwait.tt/categoryhome.aspx?catid=39",
    "http://alwatan.kuwait.tt/categoryhome.aspx?catid=35",
    "http://alwatan.kuwait.tt/categoryhome.aspx?catid=61",
    "http://alwatan.kuwait.tt/categoryhome.aspx?catid=49",
    "http://alwatan.kuwait.tt/categoryhome.aspx?catid=46",
    "http://alwatan.kuwait.tt/categoryhome.aspx?catid=41",
    "http://alwatan.kuwait.tt/categoryhome.aspx?catid=42",
    "http://alwatan.kuwait.tt/categoryhome.aspx?catid=51",
    "http://alwatan.kuwait.tt/categoryhome.aspx?catid=36",
    "http://alwatan.kuwait.tt/categoryhome.aspx?catid=44",
    "http://alwatan.kuwait.tt/categoryhome.aspx?catid=50",
         ]
#,follow=True
    rules=(Rule(LinkExtractor(allow=('id=\d{5}'),deny=('index=')) ,\
                callback='parse_news',follow=True),\
             Rule(LinkExtractor(allow=('category|yearquarter|index='),deny=('video|login|feed')),
             follow=True),
             Rule(LinkExtractor(allow=('.*'),deny=('login|writershome|advertisewithus|ZoneType')),
             callback='parse_url',follow=True),

     )

    def parse_url(self, response):
        print response.url

    def parse_news(self, response):

        url=response.url
        try:
            title=response.xpath("//font[@class='ArticlemainTitle']/text()").extract()[0]
            contents=response.xpath("//div[@class='ArticleText']").extract()[0]
        except BaseException,e:
            print e
            print url
            return

        time=response.xpath("//font[@class='WriterLink']/text()").extract()#[0]
        time=time[1]+time[2]

        ar=arItem()
        ar["title"]=title
        ar["content"]=contents
        ar["review"]=""
        ar["time"]=time
        ar["url"]=url
        return ar
