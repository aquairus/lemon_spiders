# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import hjItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class ln2Spider(CrawlSpider):
    name = "learn_2"
    allowed_domains = ["kr.300168.com"]
    start_urls = [
"http://kr.300168.com/xuexi/list-12.html",
"http://kr.300168.com/xuexi/list-13.html",

 ]

    rules=(
            Rule(LinkExtractor(allow=('list-\d+-\d'),deny=('entertain')) ,\
                        callback='parse_url',follow=True),
    Rule(LinkExtractor(allow=('show'),deny=('enterdsadsa')) ,\
                callback='parse_al'),


     )

    def parse_url(self, response):
        #print response.url
        pass
    def parse_al(self, response):
        url=response.url
        name=response.xpath("//h1[@class='title']/text()").extract()[0]

        krs=response.xpath("//div[@class='langs_en']/text()").extract()
        zhs=response.xpath("//div[@class='langs_cn']/text()").extract()
        if len(krs) and len(krs)==len(zhs):

            pair_num=len(krs)
            content=[]
            for i in range(pair_num):
                pair={}
                pair["kr"]=krs[i]
                pair["zh"]=zhs[i]

                content.append(pair)
        else:
            krs=response.xpath("//div[@class='para original']/text()").extract()
            zhs=response.xpath("//div[@class='para translate grey']/text()").extract()
            if len(krs) and len(krs)==len(zhs):
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
