from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import cptItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re

regex = re.compile(r"novelId=(\d*)&volumeNo=(\d*)")
tiele_re = re.compile(r"novelId=(\d*)")

class krSpider(CrawlSpider):
    name = "kr"
    allowed_domains = ["novel.naver.com"]
    start_urls = [#"http://novel.naver.com/challenge/genre.nhn",
    "http://novel.naver.com/best/genre.nhn",
        # "http://novel.naver.com/webnovel/weekday.nhn",
        #  "http://novel.naver.com/webnovel/weekdayList.nhn",
     ]

    rules=(Rule(LinkExtractor(allow=('(.*?)novelId=\d*$')),\
    follow=True ),\
            Rule(LinkExtractor(allow=('(.*?)volumeNo=\d*$')), \
            callback='parse_chapter',follow=True ),\
            Rule(LinkExtractor(allow=('(.*?)page=\d*$')) ),
            Rule(LinkExtractor(allow=('(.*?)genre=\d*$')) ),

     )



    def parse_chapter(self, response):

        m=regex.search(response.url)

        novelId=m.group(1)
        volumeNo=m.group(2)
        review=""

        try:
            text=response.css('div[id=content]').extract()[0]
            soup=BeautifulSoup(text,"lxml")
            title=soup.find('a',class_="tit_book N=a:flt.end")
            div=soup.find('div',class_="detail_view_content ft15")
            plist=div.find_all('p')
            for p in plist:
                review=review+"<p>"+p.text+"</p>"
        except BaseException, e:
            print e
            pass

        item=cptItem()
        item["volumeNo"]=volumeNo
        item["novelId"]=novelId
        item["review"]=review
        item["title"]=title.text

        return item
