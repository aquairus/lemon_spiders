from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import NvItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

class NvSpider(CrawlSpider):
    name = "nv"
    base_url ="http://kin.naver.com"
    allowed_domains = ["kin.naver.com"]
    start_urls = [
        "http://kin.naver.com/qna/list.nhn?m=ing&dirId=0",
         "http://kin.naver.com/qna/list.nhn?m=kinup&dirId=0",
         "http://kin.naver.com/qna/list.nhn?m=directoryExpert&dirId=0",
     ]

    rules=(Rule(LinkExtractor(allow=('(.*?)page=.*')),follow=True),\
     Rule(LinkExtractor(allow=('(.*?)docId.*')), callback='parse_item',follow=True ),
     )





    def parse_item(self, response):

        contents=response.css('h3[class=_endTitleText]::text').extract()
        try:
            content=contents[0].lstrip().rstrip()
        except BaseException, e:
		    content=""

        review=""
        try:
            text=response.css('div[id=content]').extract()[0]
            soup=BeautifulSoup(text,"lxml")
            ansList=soup.find_all('div',class_="_endContentsText")
            for ans in ansList[1:]:
                review=review+ans.text+"<p>"
        except BaseException, e:
            pass

        item =NvItem()
        item['content']=content
        item['review']=review
        return item
