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

class ar3Spider(CrawlSpider):
    name = "ar3"
    allowed_domains = ["alqabas.com"]
    start_urls = ["http://alqabas.com",
    "http://alqabas.com/category/حول-العالم/",
    "http://alqabas.com/category/ثقافة-وفنون/",
    "http://alqabas.com/category/كتاب-وآراء/",
    "http://alqabas.com/category/المرأة/",
    "http://alqabas.com/category/القبس-الدولي/",
    "http://alqabas.com/category/رياضة/",
    "http://alqabas.com/category/اقتصاد/",
    "http://alqabas.com/category/أمن-ومحاكم/",
    "http://alqabas.com/category/مجلس-الأمة/",
    "http://alqabas.com/category/محليات/",
    "http://alqabas.com/خريطة-الموقع/",

     ]
#,follow=True
    rules=(Rule(LinkExtractor(allow=('/\d{3}'),deny=('201\d')) ,\
                follow=True,callback='parse_news'),\
             Rule(LinkExtractor(allow=('category|tag|date|page|author'),deny=('video|login|feed')),
             follow=True),
             Rule(LinkExtractor(allow=('.*'),deny=('cvideo|login|feed|email')),
             callback='parse_url',follow=True),

     )

    def parse_url(self, response):
        print response.url

    def parse_news(self, response):

        url=response.url

        try:
            title=response.xpath("//span[@itemprop='name']/text()").extract()[0].strip()
            contents=response.xpath("//div[@class='entry']/p").extract()
        except BaseException,e:
            print e
            print url
            return
        time=response.xpath("//span[@class='tie-date']/text()").extract()[0]

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
