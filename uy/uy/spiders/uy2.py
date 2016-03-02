from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import uyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup


class uy2Spider(CrawlSpider):
    name = "uy2"
    allowed_domains = ["uyghur.news.cn"]
    start_urls = ["http://uyghur.news.cn"
     ]

    rules=(Rule(LinkExtractor(allow=('news(.*?)c_\d*')) ,\
                callback='parse_news'),
             Rule(LinkExtractor(allow=('news')),\
              callback='parse_url')

     )


    def parse_url(self, response):
        print response.url


    def parse_news(self, response):

        url=response.url
        print url
        # try:
        #     title=response.xpath('//h2/text()').extract()[0].strip()
        # except BaseException,e:
        #     print e
        #     print url
        #     return

        # time=response.xpath("//span[@id='Time']/text()").extract()[0]
        # content=response.xpath("//div[@id='Content']").extract()[0]
        # content=p_re.sub("",content)
        # content=orz_re.sub("",content)
        # content=s_re.sub("",content)
        # content=r_re.sub("",content)

        # uy=uyItem()
        # uy["title"]=title
        # uy["content"]=content
        # uy["review"]=""
        # uy["time"]=time
        # uy["url"]=url
        # return uy
