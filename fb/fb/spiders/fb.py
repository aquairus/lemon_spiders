from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import fbItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class fbSpider(CrawlSpider):
    name = "fb"
    allowed_domains = ["m.facebook.com"]
    start_urls = [
         "https://m.facebook.com/profile.php?v=friends&id=100005145335207",
     ]

    rules=(Rule(LinkExtractor(allow=('people|profile')),follow=True),\
    Rule(LinkExtractor(allow=('v=friends')),callback='parse_item',follow=True),\
     )





    def parse_item(self, response):

        names=response.xpath("//a[@class='cb']/text()").extract()
        for name in names:
            print name
        url=response.url
        print url

        # item =fbItem()
        # item['name']=name
        # item['url']=url
        # return item
