from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import xmItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class xmSpider(CrawlSpider):
    name = "xm0"
    allowed_domains = ["ximalaya.com"]
    start_urls = ["http://www.ximalaya.com/dq/all",

     ]

    rules=(
            Rule(LinkExtractor(allow=('album/\d+'),deny=('entertain')) ,\
                        callback='parse_al',follow=True),
    Rule(LinkExtractor(allow=('/dq/'),deny=('enterdsadsa')) ,\
                follow=True),


     )

    def parse_url(self, response):
        print response.url

    def parse_al(self, response):

        url=response.url

        category=response.xpath("//div[@class='detailContent_category']/a/text()").extract()[0]
        name=response.xpath("//div[@class='detailContent_title']/h1/text()").extract()[0]
        count=response.xpath("//div[@class='detailContent_playcountDetail']/span/text()").extract()[0]
        tags=response.xpath("//div[@class='tagBtnList']//span/text()").extract()
        username=response.xpath("//div[@class='username']/text()").extract()[0].strip()
        tag_list=[]
        album_list=[]
        album=response.xpath("//a[@class='title']/text()").extract()

        for tag in tags:
            tag_list.append(tag)
        for alb in album:
            album_list.append(alb)
        xm=xmItem()
        xm["name"]=name
        xm["username"]=username
        xm["count"]=count
        xm["category"]=category
        xm["tag_list"]=tag_list
        xm["album_list"]=album_list
        xm["url"]=url[24:]
        return xm
