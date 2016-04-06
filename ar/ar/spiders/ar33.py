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

class ar33Spider(CrawlSpider):
    name = "ar33"
    allowed_domains = ["aawsat.com"]
    start_urls = ["http://aawsat.com",
         ]

    rules=(Rule(LinkExtractor(allow=('section|page'),deny=('video|login|feed|image|article')),
                callback='parse_url',follow=True),
    Rule(LinkExtractor(allow=('article/\d+'),deny=('helloworld|nfriend|print')) ,\
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
            title=response.css("h2::text").extract()[0].strip()
            content=response.css("div[class*=body]").extract()[0]

            time=response.css("div[id*=date]::text").extract()[0]
            reviews=response.css("div[class*=field]::text").extract()
        except BaseException,e:
            print e
            print url
            return

        review=""
        for r in reviews:
            r=r.strip()
            if r:
                review=review+r+"<p>"
                print r
        content=tag_re.sub(" ",content)

        ar=arItem()
        ar["title"]=title
        ar["content"]=content
        ar["review"]=review
        ar["time"]=time
        ar["url"]=url
        return ar
