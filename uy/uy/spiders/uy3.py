from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import uyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
time_re = re.compile(r".*?: ")

class uy3Spider(CrawlSpider):
    name = "uy3"
    allowed_domains = ["tograk.com"]
    start_urls = ["http://tograk.com",

     ]


    rules=(Rule(LinkExtractor(allow=('catid=(13|88|6|11|195|17|31|38|44|12|15)&'),deny=('lists')) ,\
                callback='parse_news',follow=True),
            Rule(LinkExtractor(allow=('catid=(13|88|6|11|195|17|31|38|44|12|15)'),deny=('catid=(114|115|61|139|136|138|121|125)')) ,\
                callback='parse_url',follow=True),
            Rule(LinkExtractor(allow=('.*'),deny=('search|Archiver|qq|bbs|catid|mahsustema')),
                callback='parse_url'),

     )

    def parse_url(self, response):
        print response.url


    def parse_news(self, response):
        url=response.url

        try:
            title=response.css('div[class=showrighttile]::text').extract()[0]
        except BaseException,e:
            print e
            print url
            return
        time=response.css('div[class=showrightcount]::text').extract()[0]
        time=str(time[40:70])
        time=time_re.sub("",time).strip()
        #print time

        content=response.xpath("//div[@class='showorux']").extract()[0]

        uy=uyItem()
        uy["title"]=title
        uy["content"]=content
        uy["review"]=""
        uy["time"]=time
        uy["url"]=url
        return uy
