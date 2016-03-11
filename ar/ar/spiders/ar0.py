# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import arItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class arSpider(CrawlSpider):
    name = "ar0"
    allowed_domains = ["arabic.cnn.com"]
    start_urls = ["http://arabic.cnn.com",
    "http://arabic.cnn.com/sport",
    "http://arabic.cnn.com/scitech",
    "http://arabic.cnn.com/business",
    "http://arabic.cnn.com/special_reports/live_smart",
    "http://arabic.cnn.com/special_reports/vital_signs",
    "http://arabic.cnn.com/special_reports/one_square_meter",
    "http://arabic.cnn.com/الكويت",
    "http://arabic.cnn.com/اليمن",
    "http://arabic.cnn.com/سلطنة-عمان",
    "http://arabic.cnn.com/قطر",
    "http://arabic.cnn.com/الأردن",
    "http://arabic.cnn.com/العراق",
    "http://arabic.cnn.com/سوريا",
    "http://arabic.cnn.com/لبنان",
    "http://arabic.cnn.com/مصر",
    "http://arabic.cnn.com/الجزائر",
    "http://arabic.cnn.com/المغرب",
    "http://arabic.cnn.com/تونس",
    "http://arabic.cnn.com/ليبيا",
    "http://arabic.cnn.com/عائض-القرني",
    "http://arabic.cnn.com/أسامة-بن-لادن",
    "http://arabic.cnn.com/داعش",

    "http://arabic.cnn.com/حزب-الله",
    "http://arabic.cnn.com/الحرب-السورية",
    "http://arabic.cnn.com/gallery",
    "http://arabic.cnn.com/world",
    "http://arabic.cnn.com/middle_east",
    "http://arabic.cnn.com/travel",
     ]

    rules=(Rule(LinkExtractor(allow=('\d+/\d+/\d+'),deny=('entertain')) ,\
                callback='parse_news'),
            Rule(LinkExtractor(allow=('\d+/\w+/\d+/\d+'),deny=('entertain')) ,\
                        callback='parse_news'),
             Rule(LinkExtractor(allow=('page|%'),deny=('entertain|privacy|terms|archive')),
             follow=True),
             Rule(LinkExtractor(allow=('.*'),deny=('entertain|privacy|terms|archive')),
             follow=True),

     )

    def parse_url(self, response):
        print response.url

    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.xpath("//h1[@class='news-headline-desktop']/text()").extract()[0].strip()
            content=response.xpath("//div[@class='article-content']//div").extract()[0]
        except BaseException,e:
            try:
                content=response.xpath("//div[@class='body field']").extract()[0]
            except BaseException,e:
                print e
                print url
                return
        time=response.xpath("//span[@class='news-date']/text()").extract()[0].strip()

        ar=arItem()
        ar["title"]=title
        ar["content"]=content
        ar["review"]=""
        ar["time"]=time
        ar["url"]=url
        return ar
