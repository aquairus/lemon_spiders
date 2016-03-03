from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import uyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from time import sleep
from selenium import webdriver



time_re = re.compile(r".*?: ")




class uy6Spider(CrawlSpider):
    name = "uy6"
    allowed_domains = ["www.nur.cn"]
    start_urls = ["http://www.nur.cn/index.shtml",
     ]


    rules=(Rule(LinkExtractor(allow=('news.*?/\d+/'),deny=('login|hash')) ,\
                callback='parse_news'),

             Rule(LinkExtractor(allow=('catid'),deny=('fuck|special')),
             callback='parse_cat',follow=True),

             Rule(LinkExtractor(allow=('.*'),deny=('fuck|news|apk|login|register|zhongduan')),
             callback='url',follow=True),

     )


    def parse_url(self, response):
        pass
        #print response.url


    def parse_cat(self, response):

        urls=[]
        url=response.url
        driver = webdriver.PhantomJS('phantomjs')
        driver.get(url)
        for i in xrange(24):
            driver.find_element_by_class_name("more").click()
        links=driver.find_elements_by_xpath("//div[@class='tur_news']//a")
        for link in links:
        	urls.append(link.get_attribute("href"))
        driver.close()
        for url in urls:
            print url
            yield Request(url,self.parse_news)




    def parse_news(self, response):

        url=response.url
        print url
        # try:
        #     title=response.xpath('//h1/text()').extract()[0].strip()
        # except BaseException,e:
        #     print e
        #     print url
        #     return
        #
        # time=response.xpath("//p[@class='uquri']/span/text()").extract()[0]
        # time=str(time[48:90])
        # time=time_re.sub("",time).strip()
        #
        # content=response.xpath("//div[@class='content']").extract()[0]
        #
        # uy=uyItem()
        # uy["title"]=title
        # uy["content"]=content
        # uy["review"]=""
        # uy["time"]=time
        # uy["url"]=url
        # return uy
