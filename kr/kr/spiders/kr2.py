from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import cptItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
import re


regex = re.compile(r"novelId=(\d*)&volumeNo=(\d*)")
page_re = re.compile(r"\[(\d*)\]")
tag_re = re.compile(r"<div.*?>|<font.*?>|<span.*?>|<strong>|</strong>|</span>|</font>|</div>")
p_re = re.compile(r"<p.*?>")



class kr2Spider(CrawlSpider):
    name = "kr2"
    allowed_domains = ["ijakga.com"]
    start_urls = ["http://www.ijakga.com/",\
                 "http://www.ijakga.com/series/",\
                 "http://www.ijakga.com/usr/",\
                # "http://novel.naver.com/webnovel/weekdayList.nhn",\
     ]

    rules=(Rule(LinkExtractor(allow=('(.*?)ilog$')),\
                callback='parse_chapter',follow=True ),
            Rule(LinkExtractor(allow=('(.*?)asp\\?sid=\d*$'),deny=("intro|review")), \
                follow=True ),
             Rule(LinkExtractor(allow=('(series|usr)(.*?)asp$'),deny=('login')),\
                follow=True ),
             Rule(LinkExtractor(allow=('page'),deny=('login|ndate')),\
                follow=True ),
     )

    def parse_url(self, response):
        #pass
        print response.url

    def parse_chapter(self, response):

        title=response.xpath("//div[@class='tit_area']/h3/text()").extract()
        if title:
            title=title[0].strip()
        else:
            return
        page=response.xpath("//div[@class='title']/h3/text()").extract()
        m=page_re.search(page[0])
        volumeNo=m.group(1)

        raw_content=response.xpath("//div[@class='content']").extract()
        first_content=tag_re.sub("<br>",raw_content[0])
        review=p_re.sub("<p>",first_content)

        novelId=hash(title)

        item=cptItem()
        item["volumeNo"]=volumeNo
        item["novelId"]=novelId
        item["review"]=review
        item["title"]=title
        return item
