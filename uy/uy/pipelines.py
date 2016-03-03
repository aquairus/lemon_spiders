# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import json
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )

import re
dorp_re = re.compile(r"\\r|<font.*?>|<!--.*?-->|<td.*?>|</td>|<center.*?>|<iframe.*?>|</iframe>|<span.*?>|</span>|<tbody.*?>|</tbody>|</font>|<center>|<img.*?>|</img>|<stript.*?>|</stript>|<meta.*?>|</meta>|</center>|<a.*?>|</a>|<shapetype.*?/shapetype>|<strong.*?>|</strong>|<embed.*?/embed>|<li.*?>|</li>|<ul.*?>|</ul>|</div>|<div.*?>")

r_re = re.compile(r"(\\n)+|\n+")
br__re = re.compile(r"(<br>)+")
br_re = re.compile(r"<br.*?>")
s_re = re.compile(r"\s+")
p_re = re.compile(r"<p.*?>")
t_re = re.compile(r"(\\t)+|t311|\t2,736|t1")




class uyPipeline(object):
    def open_spider(self, spider):
        self.of=open("../../"+spider.name+".txt",'w+')

    def process_item(self, item, spider):
        dic=dict(item)
        dic["type"]="news"
        self.of.write(json.dumps(dic, ensure_ascii=False)+"\n")


    def close_spider(self, spider):
        self.of.close()


class contentPipeline(object):

    def process_item(self, item, spider):
        newline=item["content"]

        newline=p_re.sub("<p>",newline)
        newline=br_re.sub("<br>",newline)
        newline=br__re.sub("<br>",newline)
        newline=dorp_re.sub("",newline)
        newline=s_re.sub(r" ",newline)
        newline=t_re.sub(r"\\t",newline)
        newline=r_re.sub(r"\\n",newline)
        newline=r_re.sub(r"\\n",newline)

        item["content"]=newline
        return item


class mergePipeline(object):

    def __init__(self):
        self.content = dict()
        self.total = dict()
        self.answers=dict()


    def process_item(self, item, spider):
        tid=item["tid"]

        if "total" in item:
            if item["total"]=="1":
                print "short topic"
                return item
            else:
                self.content[tid]=item.copy()
                self.total[tid]=item["total"]
                raise DropItem("content")


        if not tid in self.answers:
            self.answers[tid]={}

        pid=int(item["pid"])
        self.answers[tid][pid]=item["answers"]

        keys=self.answers[tid].keys()

        if len(keys)+1==int(self.total[tid]):
            for (v,c) in self.answers[tid].items():
                self.content[tid]["answers"]=\
                self.content[tid]["answers"]+c
            douban=self.content[tid].copy()
            self.total.pop(tid)
            self.answers.pop(tid)
            self.content.pop(tid)
            print "long!!"
            return douban
        else:
            raise DropItem("answers")
