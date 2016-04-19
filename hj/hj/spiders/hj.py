# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ..items import hjItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import re
dorp_re = re.compile(r"\\r|<font.*?>|<!--.*?-->|\{.*?\}|TRS_Editor|<td.*?>|</td>|<center.*?>|<iframe.*?>|</iframe>|<span.*?>|</span>|<tbody.*?>|</tbody>|</font>|<center>|<img.*?>|</img>|<stript.*?>|</stript>|<meta.*?>|</meta>|</center>|<a.*?>|</a>|<shapetype.*?/shapetype>|<strong.*?>|</strong>|<embed.*?/embed>|<li.*?>|</li>|<ul.*?>|</ul>|</div>|<div.*?>")
dorp2_re = re.compile(r"<style.*?>|</style>|/style>|P|DIV|TD|TH|SPAN|FONT|UL|LI|A|<u>|</u>")


class hjSpider(CrawlSpider):
    name = "hj"
    allowed_domains = ["kr.hujiang.com"]
    start_urls = [
"http://kr.hujiang.com/new/tag/韩剧中的文化/",
"http://kr.hujiang.com/new/tag/韩剧资讯/",
"http://kr.hujiang.com/new/tag/韩剧学习笔记/",
"http://kr.hujiang.com/new/tag/韩剧台词学韩语/",
'http://kr.hujiang.com/new/tag/韩国旅游景点/',
"http://kr.hujiang.com/new/tag/韩国文化全方位/",
"http://kr.hujiang.com/new/tag/看CF学韩语/",
"http://kr.hujiang.com/new/tag/赴韩旅游小贴士/",
"http://kr.hujiang.com/new/tag/明星推特学韩语/",
"http://kr.hujiang.com/new/topic/537/",
"http://kr.hujiang.com/new/topic/505/",
"http://kr.hujiang.com/new/topic/539/",
"http://kr.hujiang.com/new/topic/538/",
"http://kr.hujiang.com/new/topic/471/",
"http://kr.hujiang.com/new/c15070/",
"http://kr.hujiang.com/new/krinchina/",
"http://kr.hujiang.com/new/hanqiwenhua/",
"http://kr.hujiang.com/new/zhichanghanyu/",
"http://kr.hujiang.com/new/hanjudianying/",
"http://kr.hujiang.com/new/hanguoyinyue/",
"http://kr.hujiang.com/new/mingxingshishang/",
"http://kr.hujiang.com/new/hanguowenhua/",
"http://kr.hujiang.com/new/hanguoyinyue/",

 ]

    rules=(
            Rule(LinkExtractor(allow=('page'),deny=('entertain')) ,\
                        callback='parse_url',follow=True),
    Rule(LinkExtractor(allow=('/new/p\d'),deny=('enterdsadsa')) ,\
                callback='parse_al'),


     )

    def parse_url(self, response):
        #print response.url
        pass
    def parse_al(self, response):
        #print response.url
        url=response.url
        name=response.xpath("//div[@class='page_title']/text()").extract()[0]
    #    print name
        krs=response.xpath("//div[@class='langs_en']").extract()
        zhs=response.xpath("//div[@class='langs_cn']").extract()
        if len(krs):

            pair_num=len(krs)
            content=[]
            for i in range(pair_num):
                pair={}
                newline=krs[i]
                newline=dorp_re.sub("",newline)
                newline=dorp2_re.sub("",newline)
                pair["kr"]=newline

                newline=zhs[i]
                newline=dorp_re.sub("",newline)
                newline=dorp2_re.sub("",newline)
                pair["zh"]=newline
                content.append(pair)
        else:
            return

        hj=hjItem()
        hj["title"]=name
        hj["content"]=content
        hj["url"]=url
        return hj
