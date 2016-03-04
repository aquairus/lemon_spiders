# -*- coding: utf-8 -*-
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

             Rule(LinkExtractor(allow=('catid'),deny=('fuck|special|login')),
             callback='parse_cat',follow=True),

             Rule(LinkExtractor(allow=('special'),deny=('fuck|news|hash|login|register|zhongduan')),
             follow=True),

     )


    def __init__(self, *args, **kwargs):

        self.driver = webdriver.PhantomJS('phantomjs')
        super(uy6Spider,self).__init__(*args, **kwargs)


    def parse_url(self, response):
        print response.url




    def parse_cat(self, response):

        urls=[]
        url=response.url

        self.driver.get(url)
        for i in xrange(24):#24
            self.driver.find_element_by_class_name("more").click()
        links=self.driver.find_elements_by_xpath("//div[@class='tur_news']//a")
        for link in links:
        	urls.append(link.get_attribute("href"))

        for url in urls:
            yield Request(url,self.parse_news)




    def parse_news(self, response):

        url=response.url

        try:
            title=response.xpath('//h2/text()').extract()[0].strip()
        except BaseException,e:
            print e
            print url
            return

        time=response.xpath("//p[@class='uquri']/span/text()").extract()[3]
        time=time_re.sub("",time).strip()

        content=response.xpath("//div[@class='mazmun']").extract()[0]

        self.driver.get(url)
        review=""
        try:
            p=self.driver.find_element_by_xpath("//div[@id='loadMore']//p")
            style=p.get_attribute("style")
            next_page=style=="display: none;"
        except BaseException,e:
            next_page=None


    	while next_page:
            self.driver.find_element_by_id("loadMore").click()
            p=self.driver.find_element_by_xpath("//div[@id='loadMore']//p")
            style=p.get_attribute("style")
            next_page=style=="display: none;"

        comments=self.driver.find_elements_by_class_name("np-post-content")
        if comments:
            for cm in comments:
    			review=review+"<p>"+cm.text+"</p>"

        uy=uyItem()
        uy["title"]=title
        uy["content"]=content
        uy["review"]=review
        uy["time"]=time
        uy["url"]=url
        return uy
