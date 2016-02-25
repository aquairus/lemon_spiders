# -*- coding:utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import cptItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
import re


regex = re.compile(r"bid=(\d*)")
page_re = re.compile(r"bid=(\d*)&uid=(\d*)")
v_re = re.compile(r"(\d*)")

tag_re = re.compile(r"<div.*?>|</div>|<span.*?>|</span>|<form.*?>|</form>|<input.*?>|</input>|<i.*?>|</i>|<em.*?>|</em>")#|<i.*?>|</i>|<em>|</em>|")
p_re = re.compile(r"<p.*?>|<a.*?>|</a>|<!--.*?-->")#|<\!--.*?-->"



class kr4Spider(CrawlSpider):
    name = "kr4"
    allowed_domains = ["novel.bookpal.co.kr"]

    start_urls = [
            "http://novel.bookpal.co.kr/free",
            "http://novel.bookpal.co.kr/romance",
            "http://novel.bookpal.co.kr/fantasy",
            "http://novel.bookpal.co.kr/interest",
            "http://novel.bookpal.co.kr/allbest_all",
            "http://novel.bookpal.co.kr/serials",
     ]

    rules=(
            Rule(LinkExtractor(allow=('(.*?)uid=\d*$')), \
                callback='parse_chapter',follow=True ),
            Rule(LinkExtractor(allow=('(.*?)bid=\d*$'),deny=('3429')), \
                callback='parse_book',follow=True ),
            Rule(LinkExtractor(allow=('(.*?)page=\d*$')), \
                callback='parse_url',follow=True ),
            Rule(LinkExtractor(allow=('(.*?)genre=\d*$')), \
                callback='parse_url',follow=True ),
     )

    def __init__(self, *args, **kwargs):
        self.title_dict=dict()
        self.total_dict=dict()

        super(kr4Spider,self).__init__(*args, **kwargs)



    def parse_book(self, response):
        title=response.xpath("//span[@class='title']/text()").extract()
        if title:
            title=title[0]##.strip()
        else:
            print response.url
            return


        m=regex.search(response.url)
        novelId=m.group(1)


        span=response.xpath("//span[@class='day_month']/text()").extract()
        if span:
            total=str(span[0])
            total=total[0:-13]
        else:
            print "fuck"
            print response.url

        if total=="완":
            total=str(span[2])
            total=total[0:-13]
            if total=="완":
                total=str(span[4])
                total=total[0:-13]
            else:
                total=int(total)+1

        self.total_dict[novelId]=total
        self.title_dict[novelId]=title

    def parse_url(self, response):
        pass
        #print response.url

    def parse_chapter(self, response):

        raw_content=response.xpath("//div[@class='viewPages']").extract()
        if raw_content:
            first_content=tag_re.sub("<br>",raw_content[0])

            review=p_re.sub("<br>",first_content)
        else:
            return



        m=page_re.search(response.url)
        novelId=m.group(1)
        volumeNo=m.group(2)


        if novelId in self.title_dict:
            title=self.title_dict.pop(novelId)
        else:
            title="^_^"

        if novelId in self.total_dict:
            volumeNo=self.total_dict.pop(novelId)
        else:
            volumeNo=int(str(volumeNo))-1000000
        # print response.url
        # print volumeNo
        item=cptItem()
        item["volumeNo"]=volumeNo
        item["novelId"]=novelId
        item["review"]=review
        item["title"]=title
        return item
