# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import hjItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class lnSpider(CrawlSpider):
    name = "learn"
    allowed_domains = ["kr.tingroom.com"]
    start_urls = [
"http://kr.tingroom.com/yuedu/hymrfy/",
"http://kr.tingroom.com/yuedu/hygshi/"


 ]

    rules=(
            Rule(LinkExtractor(allow=('list'),deny=('entertain')) ,\
                        callback='parse_url',follow=True),
    Rule(LinkExtractor(allow=('/new/p\d'),deny=('enterdsadsa')) ,\
                callback='parse_al'),


     )

    def parse_url(self, response):
        #print response.url
        pass
    def parse_al(self, response):
        #print response.url
        url=response.url
        name=response.xpath("//div[@class='page_title']/text()").extract()[0]
    #    print name
        krs=response.xpath("//div[@class='langs_en']/text()").extract()
        zhs=response.xpath("//div[@class='langs_cn']/text()").extract()
        if len(krs):

            pair_num=len(krs)
            content=[]
            for i in range(pair_num):
                pair={}
                pair["kr"]=krs[i]
                pair["zh"]=zhs[i]
                content.append(pair)
        else:
            return

        hj=hjItem()
        hj["title"]=name
        hj["content"]=content
        hj["url"]=url
        return hj
