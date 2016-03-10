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
        username=response.xpath("//div[@class='username']/text()").extract()[0].strip()
  
        tag_list=[]
        album_list=[]

        try:
            tags=response.xpath("//div[@class='tagBtnList']//span/text()").extract()
            for tag in tags:
                tag_list.append(tag)
        except BaseException, e:
            pass

      


        try:
            album=response.xpath("//a[@class='title']/text()").extract()
            for alb in album:
                album_list.append(alb) 
        except BaseException, e:
            pass

        try:
            count=response.xpath("//div[@class='detailContent_playcountDetail']/span/text()").extract()[0]
        except BaseException, e:
            count="0"




        xm=xmItem()
        xm["name"]=name
        xm["username"]=username
        xm["count"]=count
        xm["category"]=category
        xm["tag_list"]=tag_list
        xm["album_list"]=album_list
        xm["url"]=url[24:]
        return xm
