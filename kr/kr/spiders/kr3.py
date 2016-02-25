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



class kr3Spider(CrawlSpider):
    name = "kr3"
    allowed_domains = ["www.confactory.co.kr"]
    start_urls = ["http://www.confactory.co.kr/",\
                 "http://www.confactory.co.kr/cf/challenge/chal01001l.jsp",\
                 "http://www.confactory.co.kr/cf/best/best01001l.jsp"
     ]

    rules=( Rule(LinkExtractor(allow=('page_count$')), \
                callback='parse_chapter',follow=True ),
            Rule(LinkExtractor(allow=('cont_sno(.*?)page_count=\d*$')), \
                callback='parse_url' ),
            Rule(LinkExtractor(allow=('(.*?)cont_sno=\d*$')),
                callback='parse_url'),
            Rule(LinkExtractor(allow=('(.*?)page_count=\d*$'),deny=("premium|ebook")), \
                callback='parse_url')
     )

    def parse_url(self, response):
        #pass
        print response.url

    def parse_chapter(self, response):
        print response.url
        return
        # title=response.xpath("//div[@class='tit_area']/h3/text()").extract()
        # if title:
        #     title=title[0].strip()
        # else:
        #     return
        # page=response.xpath("//div[@class='title']/h3/text()").extract()
        # m=page_re.search(page[0])
        # volumeNo=m.group(1)
        #
        # raw_content=response.xpath("//div[@class='content']").extract()
        # first_content=tag_re.sub("<br>",raw_content[0])
        # review=p_re.sub("<p>",first_content)
        #
        # novelId=hash(title)
        #
        # item=cptItem()
        # item["volumeNo"]=volumeNo
        # item["novelId"]=novelId
        # item["review"]=review
        # item["title"]=title
        # return item
