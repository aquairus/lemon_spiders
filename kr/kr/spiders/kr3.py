from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import cptItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
import re


regex = re.compile(r"cont_sno=(\d*)")
#page_re = re.compile(r"(\d*)")
tag_re = re.compile(r"<dd.*?>|<font.*?>|<span.*?>|<strong>|</strong>|</span>|</font>|</dd>")
p_re = re.compile(r"<p.*?>")



class kr3Spider(CrawlSpider):
    name = "kr3"
    allowed_domains = ["www.confactory.co.kr"]
    start_urls = ["http://www.confactory.co.kr/cf/home/main.jsp"
                 "http://www.confactory.co.kr/cf/best/best01001l.jsp",
                 "http://www.confactory.co.kr/cf/challenge/chal01001l.jsp"
     ]

    rules=( Rule(LinkExtractor(allow=('bbs_sno'),deny=("bbs_man_cd")), \
                callback='parse_chapter',follow=True ),
            Rule(LinkExtractor(allow=('(.*?)cont_sno=\d*$'),deny=("chal04001r")),
                follow=True),
            Rule(LinkExtractor(allow=('(.*?)page_count=\d*$'),deny=("premium|ebook|cont_sno")), \
                follow=True)
     )

    def parse_url(self, response):
        print response.url
        pass

    def parse_chapter(self, response):
        title=response.xpath("//div/h2/text()").extract()
        if title:
            title=title[0].strip()
        else:
            return
        page=response.xpath("//fieldset/span/label/text()").extract()
        volumeNo=page[0].split(":")[1][1:-1]

        #
        raw_content=response.xpath("//dd[@id='cvContents']").extract()
        review=tag_re.sub("<br>",raw_content[0])

        m=regex.search(response.url)
        novelId=m.group(1)

        item=cptItem()
        item["volumeNo"]=volumeNo
        item["novelId"]=novelId
        item["review"]=review
        item["title"]=title
        return item
