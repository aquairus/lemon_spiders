from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import uyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class uy3Spider(CrawlSpider):
    name = "uy3"
    allowed_domains = ["tograk.com"]
    start_urls = ["http://tograk.com",

     ]


    rules=(Rule(LinkExtractor(allow=('catid=(13|88|6|11|195|17|31|38|44|12|15)&')) ,\
                callback='parse_news',follow=True),
            Rule(LinkExtractor(allow=('catid=(13|88|6|11|195|17|31|38|44|12|15)'),deny=('catid=(114|115|61|139|136|138|121|125)')) ,\
                callback='parse_url',follow=True),
            Rule(LinkExtractor(allow=('.*'),deny=('search|Archiver|qq|bbs|catid|mahsustema')),
                callback='parse_url'),

     )

    def parse_url(self, response):
        print response.url


    def parse_news(self, response):
        url=response.url

        try:
            title=response.css('div[class=showrighttile]::text').extract()[0]
        except BaseException,e:
            print e
            print url
            return
        time=response.css('div[class=showrightcount]::text').extract()[0]
        #time=time[:28]
        print time[40:70]

        content=response.xpath("//div[@class='showorux']//p").extract()
        #print content

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
