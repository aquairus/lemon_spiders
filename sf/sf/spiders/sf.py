from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import *
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re



s_re = re.compile(r"\s+")
drop_re = re.compile(r"<span.*?/span>|</ul>|<ul>|<br>|<div.*?>|</div>|<a.*?a>|<li>|</li>|<span.*?>|</span>")


class sfSpider(CrawlSpider):
    name = "sf"
    #base_url ="http://kin.naver.com"
    allowed_domains = ["www.securityfocus.com"]
    start_urls = ["http://www.securityfocus.com/vulnerabilities",]

    rules=(Rule(LinkExtractor(allow=('discuss')),follow=False, callback='parse_dis'),
    #    Rule(LinkExtractor(allow=('exploit')),follow=False, callback='parse_exp'),
        Rule(LinkExtractor(allow=('bid'),deny=('solution|references|info|exploit')),follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('display_list&vendor=&version=&title=&CVE=')),follow=True ),
     )

    def parse_url(self, response):
        print response.url

    def parse_exp(self, response):
        bid=response.url[-13:-8]
        exp=response.css('div[id=vulnerability]').extract()[0]
        exp=drop_re.sub("",exp)
        exp=s_re.sub(" ",exp)
        exp=exp.strip()
        item =expItem()
        item['bid']=bid
        item['exp']=exp
        print exp
        return item


    def parse_dis(self, response):
        bid= response.url[-13:-8]
        dis=response.css('div[id=vulnerability]').extract()[0]
        dis=drop_re.sub("",dis)
        dis=s_re.sub(" ",dis)
        dis=dis.strip()

        item =disItem()
        item['bid']=bid
        item['dis']=dis
        return item





    def parse_item(self, response):
        bid= response.url[-5:]
        try:
            title=response.css('span[class=title]::text').extract()[0]
            remote=response.xpath("//tr[4]/td[2]/text()").extract()[0].strip()
            local=response.xpath("//tr[5]/td[2]/text()").extract()[0].strip()
            publish=response.xpath("//tr[6]/td[2]/text()").extract()[0].strip()
            update=response.xpath("//tr[7]/td[2]/text()").extract()[0].strip()
            vulner=response.xpath("//tr[9]/td[2]").extract()[0]
        except BaseException, e:
            print response.url
            return
        vulner=drop_re.sub("",vulner)
        vulner=s_re.sub(" ",vulner)[4:-5]


        item =sfItem()
        item['bid']=bid
        item['title']=title

        item['remote']=remote
        item['local']=local

        item['update']=update
        item['publish']=publish
        item['vulner']=vulner
        # item['dis']=dis
        return item

        # title=response.css('span[class=title]::text').extract()[0]
        # trs=response.css('tr').extract()
        # print trs[5][4:-5].strip()
        # print trs[6][4:-5].strip()
        # print trs[7][4:-5].strip()
        # print trs[8][4:-5].strip()
        # print trs[10][4:-5].strip()
