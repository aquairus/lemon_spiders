from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import uyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

class uySpider(CrawlSpider):
    name = "uy1"
    allowed_domains = ["uy.ts.cn"]
    start_urls = ["http://uy.ts.cn/news/"
     ]

    rules=(Rule(LinkExtractor(allow=('content_\d*'),deny=('wenhua|life|wenxue|cn.content')) ,\
                callback='parse_news',follow=True),
             Rule(LinkExtractor(allow=('news|homepage|zhuanti|xinjiang|13dong|topic|hlwdh|2016lianghui|posts')),\
              follow=True),
             Rule(LinkExtractor(allow=('.*'),deny=('wenhua|life|wenxue|video|cn.content')),
             follow=True),

     )

    def parse_url(self, response):
        print response.url

    def parse_news(self, response):

        url=response.url
    #    print url
        try:
            title=response.xpath('//h2/text()').extract()[0].strip()
        except BaseException,e:
            print e
            print url
            return

        time=response.xpath("//span[@id='Time']/text()").extract()[0]
        content=response.xpath("//div[@id='Content']").extract()[0]
        uy=uyItem()
        uy["title"]=title
        uy["content"]=content
        uy["review"]=""
        uy["time"]=time
        uy["url"]=url
        return uy
