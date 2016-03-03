from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import uyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
time_re = re.compile(r".*?: ")




class uy4Spider(CrawlSpider):
    name = "uy4"
    allowed_domains = ["www.izqila.com"]
    start_urls = ["http://www.izqila.com/news/",
     ]


    rules=(Rule(LinkExtractor(allow=('mazmun.*?Love_id=\d*')) ,\
                callback='parse_news'),
             Rule(LinkExtractor(allow=('news'),deny=('mazmun')),
             follow=True),

     )


    def parse_news(self, response):

        url=response.url

        try:
            title=response.xpath('//h1/text()').extract()[0].strip()
        except BaseException,e:
            print e
            print url
            return

        time=response.xpath("//p[@class='uquri']/span/text()").extract()[0]
        time=str(time[48:90])
        time=time_re.sub("",time).strip()

        content=response.xpath("//div[@class='content']").extract()[0]

        uy=uyItem()
        uy["title"]=title
        uy["content"]=content
        uy["review"]=""
        uy["time"]=time
        uy["url"]=url
        return uy
