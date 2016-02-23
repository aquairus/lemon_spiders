from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import topicItem,ansItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re

# regex = re.compile(r"novelId=(\d*)&volumeNo=(\d*)")
topic_re = re.compile(r"/topic/(\d*)/")
answers_re=re.compile(r"/topic/(\d*)/\?start=(\d*)")

class doubanSpider(CrawlSpider):
    name = "douban"
    allowed_domains = ["douban.com"]
    start_urls = ["https://www.douban.com/group/explore"
     ]

    rules=(Rule(LinkExtractor(allow=('(.*?)explore/\w*$')) ),\
            Rule(LinkExtractor(allow=('(.*?)group/\w*/$')),\
                         callback='parse_url',follow=True ),
             Rule(LinkExtractor(allow=('(.*?)\w\\?start=\d*$')),\
              callback='parse_url',follow=True),\
            Rule(LinkExtractor(allow=('(.*?)topic/\d*/$')),\
                         callback='parse_topic',follow=True ),
            Rule(LinkExtractor(allow=('(.*?)topic/\d*/\\?start=\d*00$')),\
                         callback='parse_answers',follow=True ),

     )


    def parse_url(self, response):
        print response.url
        pass


    def parse_topic(self, response):
        print response.url
        m=topic_re.search(response.url)
        tid=m.group(1)

        title=response.css('h1::text').extract()[0]
        author=response.xpath('//h3/span/a/text()').extract()[0]
        time=response.css('span[class=color-green]::text').extract()[0]

        paras=response.xpath("//div[@class='topic-content']/p/text()").extract()
        topic_content=""
        for p in paras:
            topic_content=topic_content+p+"<p>"

        try:
            text=response.css('ul[class=topic-reply]').extract()[0]
            answers=get_answers(text)
        except BaseException, e:
            answers=[]

        try:
            total=response.css('span[class=thispage]::attr(data-total-page)').extract()[0]
        except BaseException, e:
            total="1"

        topic=topicItem()
        topic["title"]=title
        topic["author"]=author
        topic["time"]=time
        topic["answers"]=answers
        topic["topic_content"]=topic_content
        topic["tid"]=tid
        topic["total"]=total
        return topic

    def parse_answers(self, response):
        print response.url
        m=answers_re.search(response.url)
        tid=m.group(1)
        pid=m.group(2)
        text=response.css('ul[class=topic-reply]').extract()[0]
        answers=get_answers(text)
        item= ansItem()
        item["tid"]=tid
        item["pid"]=pid
        item["answers"]=answers
        return item



def get_answers(text):
    answers=[]
    soup=BeautifulSoup(text,"lxml")
    replys=soup.find_all('li')
    for reply in replys:
        ans=get_ans(reply)
        answers.append(ans)
    return answers

def get_ans(li):
    ans={}
    answer=li.find("h4").a.text
    time=li.find("h4").span.text
    content=li.find("p").text
    try:
        quote_text=li.find("span",class_="short").text
    except BaseException, e:
        quote_text=""

    ans["content"]=content
    ans["quote_text"]=quote_text
    ans["time"]=time
    ans["answer"]=answer
    return ans
