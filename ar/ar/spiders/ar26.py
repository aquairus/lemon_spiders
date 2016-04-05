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
tag_re = re.compile(r"\\t+|<h1.*?>|</h1>|<a.*?>|</a>|<ul.*?>|</ul>|<div.*?>|</div>|<li.*?>|</li>|<img.*?>|<strong>|</strong>|<span.*?>|</span>")

class ar26Spider(CrawlSpider):
    name = "ar26"
    allowed_domains = ["akhbarelyaom.com"]
    start_urls = ["http://www.akhbarelyaom.com",
         ]

    rules=(Rule(LinkExtractor(allow=('cat|page'),deny=('video|login|feed|image|article')),
                callback='parse_url',follow=True),
    Rule(LinkExtractor(allow=('\d$'),deny=('helloworld|nfriend|print')) ,\
                follow=False,callback='parse_news'),
            #  Rule(LinkExtractor(allow=('.*'),deny=('video|help|login|news_details|rss|writer|image|article')),
            #   callback='parse_url'),
     )

    def parse_url(self, response):
        #print response.url
        pass

    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.css("h1[class*=title] a::text").extract()[0].strip()
            contents=response.xpath("//div[@class='entry']//p").extract()
            time=response.css("div[class*=inner] span::text").extract()[2]
        except BaseException,e:
            print e
            print url
            return

        time=response.css("div[class*=inner] span::text").extract()[2]

        content=""
        for c in contents[:-1]:
            content=content+c
        content=tag_re.sub(" ",content)
        ar=arItem()
        ar["title"]=title
        ar["content"]=content
        ar["review"]=""
        ar["time"]=time
        ar["url"]=url
        return ar
