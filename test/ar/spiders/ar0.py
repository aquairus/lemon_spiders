from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import arItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class arSpider(CrawlSpider):
    name = "ar0"
    allowed_domains = ["arabic.cnn.com"]
    start_urls = ["http://arabic.cnn.com"
     ]

    rules=(Rule(LinkExtractor(allow=('\d+/\d+/\d+'),deny=('entertain')) ,\
                callback='parse_news'),
            Rule(LinkExtractor(allow=('\d+/\w+/\d+/\d+'),deny=('entertain')) ,\
                        callback='parse_news'),
             Rule(LinkExtractor(allow=('page|%'),deny=('entertain|privacy|terms|archive')),
             follow=True),
             Rule(LinkExtractor(allow=('.*'),deny=('entertain|privacy|terms|archive')),
             follow=True),

     )

    def parse_url(self, response):
        print response.url

    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.xpath("//h1[@class='news-headline-desktop']/text()").extract()[0].strip()
            content=response.xpath("//div[@class='article-content']//div").extract()[0]
        except BaseException,e:
            try:
                content=response.xpath("//div[@class='body field']").extract()[0]
            except BaseException,e:
                print e
                print url
                return
        time=response.xpath("//span[@class='news-date']/text()").extract()[0].strip()

        ar=arItem()
        ar["title"]=title
        ar["content"]=content
        ar["review"]=""
        ar["time"]=time
        ar["url"]=url
        return ar
