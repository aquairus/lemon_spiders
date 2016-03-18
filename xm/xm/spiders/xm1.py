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
        url_list=[]
        count_list=[]

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
            urls=response.xpath("//a[@class='title']/@href").extract()
            for url in urls:
                url_list.append(url)
        except BaseException, e:
            pass


        try:
            counts=response.xpath("//span[@class='sound_playcount']/text()").extract()
            for cnt in counts:
                count_list.append(cnt)
        except BaseException, e:
            pass


        # try:
        #     count=response.xpath("//div[@class='detailContent_playcountDetail']/span/text()").extract()[0]
        # except BaseException, e:
        #     count="0"




        xm=xmItem()
        xm["ablum"]=name
        xm["author"]=username
        xm["category_1"]=category
        xm["category_2"]=tag_list

        xm["count_list"]=count_list
        xm["album_list"]=album_list
        xm["url_list"]=url_list
        xm["sount_cnt"]=len(url_list)
        return xm
