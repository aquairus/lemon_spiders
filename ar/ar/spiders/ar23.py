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
tag_re = re.compile(r"\\t+|<h1.*?>|</h1>|<a.*?>|</a>|<ul.*?>|</ul>|<div.*?>|</div>|<li.*?>|</li>|</article>|</like>")
space_re = re.compile(r"\s+")
out_re = re.compile(r"<br>&amp.*?<br>|<br>http.*?<br>|<br>.*?&gt;<br>")

class ar23Spider(CrawlSpider):
    name = "ar23"
    allowed_domains = ["tahrirnews.com"]
    start_urls = ["http://www.tahrirnews.com"]

    rules=(
    Rule(LinkExtractor(allow=('posts/\d+'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_news'),\

    )


    def parse_start_url(self,response):
        pre_url="http://www.tahrirnews.com/wiki/posts/"
        for id in xrange(111188,505425):
            url=pre_url+str(id)
            sleep(0.1)
            yield Request(url,callback=self.parse_news)

    def parse_news(self, response):

        url=response.url

        try:
            time=response.css('p[class*=time] span::text').extract()[0].strip()
            contents=response.css("div[class*=ontent]").extract()[0]
            title=response.css('h2[itemprop=headline]::text').extract()[0].strip()
            #title=response.xpath("//hn[@itemprop='headline']").extract()[0].strip()
        except BaseException,e:
            try:
                title=response.css('h1[itemprop=headline]::text').extract()[0].strip()
            except Exception as e:
                print e
                return

        contents=tag_re.sub(" ",contents)
        contents=space_re.sub(" ",contents)
        contents=out_re.sub(" ",contents)
        # print contents
        review=""
        # print title
        # print time
        ar=arItem()
        ar["title"]=title
        ar["content"]=contents
        ar["review"]=review
        ar["time"]=time
        ar["url"]=url
        return ar
