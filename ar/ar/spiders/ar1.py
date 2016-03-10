from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import arItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


class ar1Spider(CrawlSpider):
    name = "ar1"
    allowed_domains = ["maktoob.news.yahoo.com"]
    start_urls = ["https://maktoob.news.yahoo.com"
     ]

    rules=(Rule(LinkExtractor(allow=('\d{9}|.html$|sector.html$'),deny=('video|archive|slideshow|rss|photo')) ,\
                callback='parse_news',follow=True),
            #  Rule(LinkExtractor(allow=('page|%'),deny=('entertain|privacy|terms'))),
             Rule(LinkExtractor(allow=('.*'),deny=('video|slideshow|rss|login|photo')),
             follow=True),

     )

    def parse_url(self, response):
        print response.url

    def parse_news(self, response):

        url=response.url

        try:
            title=response.xpath("//h1[@class='headline']/text()").extract()[0].strip()
            contents=response.xpath("//div[@class='bd']//p").extract()
        except BaseException,e:
            print e
            print url
            return
        content=""
        for c in contents:
            content=content+c#"<p>"+c+"</p>"

        time=response.xpath("//cite[@class='byline vcard']/abbr/text()").extract()[0].strip()

        ar=arItem()
        ar["title"]=title
        ar["content"]=content
        ar["review"]=""
        ar["time"]=time
        ar["url"]=url
        return ar
