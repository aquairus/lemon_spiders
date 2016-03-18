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
time_re = re.compile(r"(\d+/)")

class ar6Spider(CrawlSpider):
    name = "ar6"
    allowed_domains = ["alarabiya.net"]
    start_urls = ["http://www.alarabiya.net",
    "http://www.alarabiya.net/last-page/archive.news.html"
    "http://www.alarabiya.net/technology/archive.news.html",
    "http://www.alarabiya.net/culture-and-art/archive.news.html",
    "http://www.alarabiya.net/medicine-and-health/archive.news.html",
    "http://www.alarabiya.net/latest-news.html",
    "http://www.alarabiya.net/alarabiya-today.html",
    "https://www.alarabiya.net/fashion-beauty/archive.news.html"]

    rules=(
    # Rule(LinkExtractor(allow=('/\d+/\d+/\d+'),deny=('program|podcast|vedio')) ,\
    #             follow=False,callback='parse_news'),\
    # Rule(LinkExtractor(allow=('currentPage'),deny=('program|vedio|podcast|stud')),
    #             follow=False,callback='parse_url'),
    Rule(LinkExtractor(allow=('.'),deny=('program|podcast|vedio')),
             follow=True, callback='parse_url'),
              )

    def parse_url(self, response):
        print response.url

    def parse_news(self, response):

        url=response.url
        print url
        # try:
        #     pass
        #     title=response.xpath("//div[@class='news_title']/text()").extract()[0]
        #     contents=response.xpath("//div[@class='news_details']//p").extract()
        # except BaseException,e:
        #     print e
        #     print url
        #     return
        #
        # time=response.xpath("//span[@class='news_date']/text()").extract()[0]
        # #print title
        # content=""
        # for c in contents:
        #     content=content+c
        #
        # ar=arItem()
        # ar["title"]=title
        # ar["content"]=content
        # ar["review"]=""
        # ar["time"]=time
        # ar["url"]=url
        # return ar
