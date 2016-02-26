# -*- coding:utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import cptItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
import re


regex = re.compile(r"sidx=(\d*)")
page_re = re.compile(r"didx=(\d*)&sidx=(\d*)")
v_re = re.compile(r"(\d*)")

tag_re = re.compile(r"<div.*?>|</div>|<span.*?>|</span>|<form.*?>|</form>|<input.*?>|</input>|<i.*?>|</i>|<em.*?>|</em>")#|<i.*?>|</i>|<em>|</em>|")
p_re = re.compile(r"<p.*?>|<a.*?>|</a>|<!--.*?-->")#|<\!--.*?-->"



class kr5Spider(CrawlSpider):
    name = "kr5"
    allowed_domains = ["www.seednovel.com"]

    start_urls = [
            "http://www.seednovel.com/main.php",
            "http://www.seednovel.com/pb/module/serial/serial_main.php?code=freenovel"
     ]

    rules=(
            Rule(LinkExtractor(allow=('didx(.*?)freenovel')),\
                callback='parse_chapter' ),
            Rule(LinkExtractor(allow=('freenovel(.*?)sidx')),\
                callback='parse_book',follow=True ),
            # Rule(LinkExtractor(allow=('(.*?)bid=\d*$'),deny=('3429')), \
            #     callback='parse_book',follow=True ),
            # Rule(LinkExtractor(allow=('(.*?)page=\d*$')), \
            #     callback='parse_url',follow=True ),
            # Rule(LinkExtractor(allow=('(.*?)genre=\d*$')), \
            #     callback='parse_url',follow=True ),
     )

    def __init__(self, *args, **kwargs):
        self.title_dict=dict()
        self.total_dict=dict()

        super(kr5Spider,self).__init__(*args, **kwargs)



    def parse_book(self, response):

        title=response.xpath("//span[@class='title']/text()").extract()[0]


        m=regex.search(response.url)
        novelId=m.group(1)


        span=response.xpath("//span[@class='didx']/text()").extract()
        if span:
            total=str(span[0])
        else:
            print "fuck"
            print response.url
            return

        self.total_dict[novelId]=total
        self.title_dict[novelId]=title

    def parse_url(self, response):
        print response.url

    def parse_chapter(self, response):
        raw_content=response.xpath("//div[@id='content']").extract()

        if raw_content:
             first_content=tag_re.sub("",raw_content[0])
             review=p_re.sub("",first_content)
        else:
            return

        m=page_re.search(response.url)
        novelId=m.group(2)
        volumeNo=m.group(1)

        if novelId in self.title_dict:
            title=self.title_dict.pop(novelId)
        else:
            title="^_^"

        if novelId in self.total_dict:
            volumeNo=self.total_dict.pop(novelId)
        else:
            volumeNo=int(str(volumeNo))-100000
        item=cptItem()
        item["volumeNo"]=volumeNo
        item["novelId"]=novelId
        item["review"]=review
        item["title"]=title
        return item
