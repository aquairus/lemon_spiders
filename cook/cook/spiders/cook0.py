
# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import cookItem
#from ajaxcrawl import driverSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from time import sleep
import re
from scrapy.http import Request


import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
tag_re = re.compile(r"\\t+|<h1.*?>|</h1>|<a.*?>|</a>|<ul.*?>|</ul>|<span.*?>|</span>|<li.*?>|</li>|</article>|</like>|<strong>|</strong>")
space_re = re.compile(r"\s+")
out_re = re.compile(r"<br>&amp.*?<br>|<br>http.*?<br>|<br>.*?&gt;<br>")

class cook0Spider(CrawlSpider):
    name = "cook0"
    allowed_domains = ["www.cookbooks.com"]
    start_urls = ["http://www.cookbooks.com/cookbooks_recipes/index.asp"]

    rules=(
    Rule(LinkExtractor(allow=('id=\d'),deny=('program|podcast|video|error')) ,\
                follow=True,callback='parse_cook'),\

    )


    def parse_start_url(self,response):

        pre_url="http://www.cookbooks.com/cookbooks_recipes/Recipe-Details.asp?id="
        for id in xrange(400000,1085642):
            url=pre_url+str(id)
            ##print url
            sleep(0.2)
            yield Request(url,callback=self.parse_cook)



    def parse_cook(self, response):
        url=response.url
        try:
            #title=response.css("h2::text").extract()[0].strip()
            title=response.css("font[size='5']::text")[0].extract()
            ingres=response.css("span[class*=H1]").extract()
            recipes=response.css("p[class*=H1]").extract()
            # reviews=response.css("p[class=body]::text").extract()
        except BaseException,e:
            print e
            print url
            return
        ingre=tag_re.sub("",ingre)
        recipe=tag_re.sub("",recipe)
        # print title[1]
        # print ingre
        # print recipe
        # content=""
        recipe=""
        for r in recipes:
            recipe=recipe+r

        ingre=""
        for i in ingres:
            ingre=ingre+i
        #content=tag_re.sub("",content)
        # content=space_re.sub(" ",content)
        # content=out_re.sub(" ",content)
        #
        # review=""
        # for r in reviews:
        #     review=review+r.strip()+"<p>"
        #
        #
        #
        #
        cook=cookItem()
        cook["title"]=title
        cook["ingredient"]=ingre
        cook["recipe"]=recipe
        cook["url"]=url
        return cook
