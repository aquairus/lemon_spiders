from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import uyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
time_re = re.compile(r".*?: ")


class uy2Spider(CrawlSpider):
    name = "uy2"
    allowed_domains = ["uynews.com"]
    start_urls = ["http://www.uynews.com",
     ]


    rules=(Rule(LinkExtractor(allow=('mazmun_\d*')) ,\
                callback='parse_news'),
             Rule(LinkExtractor(allow=('tur'),deny=('about|salon|elan|app|PageSpeed|mazmun|cn/view|mobile|radio|xjtv')),
             follow=True),

     )

    def parse_url(self, response):
        pass
        #print response.url


    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.xpath('//h1/text()').extract()[0].strip()
        except BaseException,e:
            print e
            print url
            return
        #print title
        time=response.xpath("//p[@class='uquri']/span/text()").extract()[0]
        time=str(time[68:100])
        time=time_re.sub("",time).strip()

        content=response.xpath("//div[@class='content']").extract()[0]
        uy=uyItem()
        uy["title"]=title
        uy["content"]=content
        uy["review"]=""
        uy["time"]=time
        uy["url"]=url
        return uy
