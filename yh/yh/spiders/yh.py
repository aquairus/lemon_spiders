from scrapy.spiders import Spider
from scrapy.selector import Selector

from ..items import qItem,aItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider
import re


ques_re = re.compile(r"qid=(.{21})")
ans_re = re.compile(r"page=(.)&qid=(.{21})")


class yhSpider(RedisSpider,CrawlSpider):
    name = "yh"
    allowed_domains = ["answers.yahoo.com"]
    start_urls = ["https://answers.yahoo.com",
     ]


    rules=(
        Rule(LinkExtractor(allow=('page=[^1]'),deny=('sort|rss')),
                callback='parse_ans',follow=True ),
        Rule(LinkExtractor(allow=('sid=\d*$'),deny=("rss")),\
                callback='parse_url',follow=True ),
        Rule(LinkExtractor(allow=('qid=.{21}$'),deny=("rss")),\
                callback='parse_ques',follow=True ),

     )

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.alowed_domains = filter(None, domain.split(','))
        super(yhSpider, self).__init__(*args, **kwargs)

    def parse_url(self, response):
        pass


    def parse_ans(self, response):
        m=ans_re.search(response.url)
        pid=m.group(1)
        qid=m.group(2)
        ans=response.css("span[class=ya-q-full-text]::text").extract()
        review=""
        for a in ans:
            review=review+a+"<p>"
        item= aItem()

        item["review"]=review
        item["qid"]=qid
        item["pid"]=pid

    #    print len(review)
        return item

    def parse_ques(self, response):
        m=ques_re.search(response.url)
        qid=m.group(1)

        try:
            title=response.css('h1::text').extract()[0].lstrip().rstrip()
        except BaseException, e:
            title=""
            return


        ans=response.css("span[class=ya-q-full-text]::text").extract()
        review=""
        for a in ans:
            review=review+a+"<p>"
        item= qItem()
        item["content"]=title
        item["review"]=review
        item["qid"]=qid
        return item
