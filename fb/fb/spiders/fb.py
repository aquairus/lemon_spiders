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
    start_urls = [s
         "https://m.facebook.com/profile.php?v=friends&id=100005145335207",
     ]

    rules=(Rule(LinkExtractor(allow=('people|profile')), callback='parse_item',follow=True),\
    Rule(LinkExtractor(allow=('friends')),follow=True),\
     )





    def parse_item(self, response):

        name=response.css('div[class=bq] strong::text').extract()
        print name
        url=response.url
        print url

        item =fbItem()
        item['name']=name
        item['url']=url
        return item
