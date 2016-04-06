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
tag_re = re.compile(r"\\t+|<h1.*?>|</h1>|<a.*?>|</a>|<ul.*?>|</ul>|<div.*?>|</div>|<li.*?>|</li>|</article>|</like>|<strong>|</strong>|<iframe.*?/iframe>")
space_re = re.compile(r"\s+")
out_re = re.compile(r"<br>&amp.*?<br>|<br>http.*?<br>|<br>.*?&gt;<br>")

class ar28Spider(CrawlSpider):
    name = "ar28"
    allowed_domains = ["maannews.net"]
    start_urls = ["http://maannews.net"]

    rules=(
    Rule(LinkExtractor(allow=('id=\d+$'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_news'),\

    )


    def parse_start_url(self,response):
        pre_url="http://maannews.net/Content.aspx?id="
        for id in xrange(11111,839126):
            url=pre_url+str(id)
            sleep(0.2)
            yield Request(url,callback=self.parse_news)

    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.css("h1[class*=title]::text").extract()[0].strip()
            time=response.css('div[class=stamp]::text').extract()[0].strip()
            content=response.css("div[class*=Body]").extract()[0]


        except BaseException,e:
            print e
            return


        content=tag_re.sub("",content)
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
