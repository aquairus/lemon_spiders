from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import uyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re

p_re = re.compile(r"<br.*?>|<font.*?>|</font>|<span>|</span>|<strong>|</strong>|<img.*?>|<center>.*?</center>|<div.*?>|</div>|<a.*?>|</a>|</br>")
orz_re = re.compile(r"<p.*?>|</p>|<!--.*?-->")

r_re = re.compile(r"\\r\\n|(\\n)+|\n+")
s_re = re.compile(r"\s+")


class uySpider(CrawlSpider):
    name = "uy1"
    allowed_domains = ["uy.ts.cn"]
    start_urls = ["http://uy.ts.cn/news/"
     ]

    rules=(Rule(LinkExtractor(allow=('news(.*?)content_\d*')) ,\
                callback='parse_news',follow=True),
             Rule(LinkExtractor(allow=('news')),\
              follow=True)

     )




    def parse_news(self, response):

        url=response.url
        try:
            title=response.xpath('//h2/text()').extract()[0].strip()
        except BaseException,e:
            print e
            print url
            return

        time=response.xpath("//span[@id='Time']/text()").extract()[0]
        content=response.xpath("//div[@id='Content']").extract()[0]
        content=p_re.sub("",content)
        content=orz_re.sub("",content)
        content=s_re.sub("",content)
        content=r_re.sub("",content)

        uy=uyItem()
        uy["title"]=title
        uy["content"]=content
        uy["review"]=""
        uy["time"]=time
        uy["url"]=url
        return uy
