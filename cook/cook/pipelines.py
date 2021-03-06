# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import json
import sys
from pymongo import MongoClient


reload(sys)
sys.setdefaultencoding( "utf-8" )

import re
dorp_re = re.compile(r"\\r|<font.*?>|<!--.*?-->|\{.*?\}|TRS_Editor|<td.*?>|</td>|<center.*?>|<iframe.*?>|</iframe>|<span.*?>|</span>|<tbody.*?>|</tbody>|</font>|<center>|<img.*?>|</img>|<scr.*?ipt>|<meta.*?>|</meta>|</center>|<a.*?>|</a>|<shapetype.*?/shapetype>|<strong.*?>|</strong>|<embed.*?/embed>")
dorp2_re = re.compile(r"<style.*?>|</style>|/style>|P|DIV|TD|TH|SPAN|FONT|UL|LI|A|\.|<em>|<h5>|</h5>|<h4>|</h4>|ShcookeFacebookEmailGoogle|LinkedInTwitter|<li.*?>|</li>|<ul.*?>|</ul>|</div>|<div.*?>|<b>|</b>|<scr.*?/script>")


r_re = re.compile(r"(\\n)+|\n+|(<p></p>)+")
br__re = re.compile(r"(<br>)+")
br_re = re.compile(r"<br.*?>")
s_re = re.compile(r"\s+")

p_re = re.compile(r"<p.*?>")
t_re = re.compile(r"(\\t)+|t311|\t2,736|t1")




class cookPipeline(object):
    def open_spider(self, spider):
        self.client = MongoClient('spider09', 27017)
        db=self.client.cook
        cook=db[spider.name]
        cook.create_index("url")
        #self.of=open("../"+spider.name+".txt",'w+')
        self.cnt=0




    def process_item(self, item, spider):
        dic=dict(item)
        # self.of.write(json.dumps(dic, ensure_ascii=False)+"\n")
        # self.cnt+=1
        # print self.cnt
        db=self.client.cook
        cook=db[spider.name]
        self.cnt+=1
        print self.cnt
        cook.insert(dic)



class contentPipeline(object):

    def process_item(self, item, spider):
        newline=item["recipe"]

        newline=p_re.sub("<p>",newline)
        newline=br_re.sub("<br>",newline)
        newline=br__re.sub("<br>",newline)
        newline=dorp_re.sub("",newline)
        newline=dorp2_re.sub("",newline)
        newline=s_re.sub(r" ",newline)
        newline=t_re.sub(r"\\t",newline)
        newline=r_re.sub(r"\\n",newline)
        newline=r_re.sub(r"\\n",newline)

        item["recipe"]=newline
        return item
