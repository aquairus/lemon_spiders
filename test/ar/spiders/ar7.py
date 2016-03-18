# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import arItem
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from time import sleep
import re
import Queue


#myqueue = Queue.Queue(maxsize = 10)


import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
time_re = re.compile(r"(\d+/)")
link_re = re.compile(r"(/\d+/\d+)")


class ar7Spider(CrawlSpider):
    name = "ar7"
    allowed_domains = ["www.masrawy.com"]
    start_urls = ["http://www.masrawy.com"]

    rules=(

        Rule(LinkExtractor(allow=('(Autos|Howa_w_Hya|News|Sports|Arts).*hpnav'),deny=('program|video|podcast|stud|Videos|Islameyat|664')),
                    follow=True, callback='parse_nav'),
        Rule(LinkExtractor(allow=('/\d+/\d+/\d+/\d+'),deny=('program|podcast|vedio')) ,\
                    follow=True,callback='parse_news'),\
        # Rule(LinkExtractor(allow=('hpnav'),deny=('program|video|podcast|stud|Videos|Islameyat|Jokes')),
        #             follow=True),
        # Rule(LinkExtractor(allow=('News|slides|news|ports|Autos|Howa_w_Hya|art|Arts'),deny=('program|video|podcast|stud|Islameyat|Videos|rss|Jokes')),
        #             follow=True),

              )


    def __init__(self, *args, **kwargs):
        ##driver=webdriver.Firefox()

        super(ar7Spider,self).__init__(*args, **kwargs)
        self.driver_queue=Queue.Queue()
        self.cnt=0

        driver =webdriver.PhantomJS()

        driver.set_page_load_timeout(40)
        driver.implicitly_wait(20)
        driver.set_script_timeout(20)

        self.driver_queue.put(driver)
 



    def parse_url(self, response):
        print response.url


    def parse_nav(self, response):

        driver = self.driver_queue.get()


        urls=set()
        url=response.url
        script_click="document.getElementById('MainContent_CatListingCtrl_divMore').click()"
        try:
            driver.get(url)
        except BaseException,e:
            print "fuck"

        print "try"
        try:
        	for i in xrange(2):
        		driver.execute_script(script_click)
        		sleep(1)
        except BaseException,e:
            #print e
            print "orz"
            print url

            self.driver_queue.put(driver)
            return


        try:
            links=driver.find_elements_by_tag_name("a")
        except BaseException,e:
            print "fuck"
            return

        for a in links:
            href=a.get_attribute("href")
            if (href and link_re.search(href)):
                urls.add(href)

        if not len(urls):
            print "fail:"
            print url
            return

        for url in urls:
            yield Request(url,callback=self.parse_news)
        self.driver_queue.put(driver)
        print "=="





    def parse_news(self, response):
        print "news"

        url=response.url

        try:
            pass
            title=response.xpath("//h1[@itemprop='headline']/text()").extract()[0]
            content=response.xpath("//div[@class='articleBody']").extract()[0]
        except BaseException,e:
            print e
            print url
            return

        time=response.xpath("//time[@itemprop='datePublished']/text()").extract()[0]

        ar=arItem()
        ar["title"]=title
        ar["content"]=content
        ar["review"]=""
        ar["time"]=time
        ar["url"]=url
        return ar
