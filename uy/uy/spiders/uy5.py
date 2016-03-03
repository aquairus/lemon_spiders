from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import uyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
time_re = re.compile(r".*?: ")


class uy5Spider(CrawlSpider):
    name = "uy5"
    allowed_domains = ["nur.cn"]
    start_urls = ["http://www.nur.cn/index.shtml",
     ]


    rules=(Rule(LinkExtractor(allow=('news.*?/\d+/')) ,\
                callback='parse_news',follow=True),
             Rule(LinkExtractor(allow=('.*'),deny=('eser|show|content|/\d+/')),
             follow=True),

     )

    def parse_url(self, response):
        pass
        print response.url


    def parse_news(self, response):

        url=response.url

        try:
            title=response.xpath("//p[@class='content_title']/text()").extract()[0].strip()
        except BaseException,e:
            print e
            print url
            return

        time=response.xpath("//span[@class='content_time']/text()").extract()[0]
        time=str(time[15:40])
        time=time.replace(":","",1).strip()

        content=response.xpath("//ul[@class='content_total']").extract()[0]
        uy=uyItem()
        uy["title"]=title
        uy["content"]=content
        uy["review"]=""
        uy["time"]=time
        uy["url"]=url
        return uy
