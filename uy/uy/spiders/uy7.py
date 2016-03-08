# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import uyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from time import sleep
from selenium import webdriver



time_re = re.compile(r".*?: ")




class uy7Spider(CrawlSpider):
    name = "uy7"
    allowed_domains = ["uy.hongshannet.cn"]
    start_urls = ["http://uy.hongshannet.cn",
     ]


    rules=(

        Rule(LinkExtractor(allow=('t.*?_.*?html'),deny=('index')) ,\
                    callback='parse_news',follow=True),

             Rule(LinkExtractor(allow=('/$'),deny=('veatlion|t201|st')),
             follow=True),
     )


    # def __init__(self, *args, **kwargs):
    #
    #     self.driver = webdriver.PhantomJS('phantomjs')
    #     super(uy7Spider,self).__init__(*args, **kwargs)


    def parse_url(self, response):

        print response.url




    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.xpath("//div[@id='doctitle']/p/text()").extract()[0].strip()
        except BaseException,e:
            print e
            print url
            return

        time=response.xpath("//div[@id='docdate']/span/text()").extract()[1]
        time=time_re.sub("",time).strip()

        content=response.xpath("//div[@class='TRS_Editor']").extract()[0]

        uy=uyItem()
        uy["title"]=title
        uy["content"]=content
        uy["review"]=""
        uy["time"]=time
        uy["url"]=url
        return uy
