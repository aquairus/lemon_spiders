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

class ar30Spider(CrawlSpider):
    name = "ar30"
    allowed_domains = ["al-sharq.com"]
    start_urls = ["http://al-sharq.com"]

    rules=(
    Rule(LinkExtractor(allow=('news/details/\d+'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_news'),\

    )


    def parse_start_url(self,response):
        pre_url="http://al-sharq.com/news/details/"
        for id in xrange(213115,413115):
            url=pre_url+str(id)
            sleep(0.5)
            yield Request(url,callback=self.parse_news)

    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.css("h1::text").extract()[0].strip()
            time=response.css('span[class*=date]::text').extract()[0].strip()
            contents=response.css("artical[class*=artcl] p::text").extract()


        except BaseException,e:
            print e
            return



        content=""
        for c in contents:
            content=content+c
        content=tag_re.sub(" ",content)
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
