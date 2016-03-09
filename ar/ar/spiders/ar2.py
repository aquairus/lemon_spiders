from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import arItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
# import sys
# reload(sys)
# sys.setdefaultencoding( "utf-8" )

time_re = re.compile(r"(\d+/)")

class ar2Spider(CrawlSpider):
    name = "ar2"
    allowed_domains = ["aljazeera.net"]
    start_urls = ["http://www.aljazeera.net"
     ]

    rules=(Rule(LinkExtractor(allow=('/\d+/\d+/\d+/'),deny=('video|archive|slideshow|rss')) ,\
                callback='parse_news',follow=True)

             Rule(LinkExtractor(allow=('.*'),deny=('video|slideshow|rss|login')),
             follow=True),

     )

    def parse_url(self, response):
        print response.url

    def parse_news(self, response):

        url=response.url
        #print url
        try:
            title=response.xpath("//h1[@class='heading-story']/text()").extract()[0].strip()
            contents=response.xpath("//div[@id='DynamicContentContainer']/p").extract()
        except BaseException,e:
            print e
            print url
            return
        #print title

        m=time_re.findall(url)
        time=m[0]+m[1]+m[2]

        content=""
        for c in contents:
            content=content+c#"<p>"+c+"</p>"

        ar=arItem()
        ar["title"]=title
        ar["content"]=content
        ar["review"]=""
        ar["time"]=time
        ar["url"]=url
        return ar
