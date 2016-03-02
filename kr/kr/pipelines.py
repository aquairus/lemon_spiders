# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from scrapy.exceptions import DropItem
import json
from items import krItem
import time
import os
import re

dorp_re = re.compile(r"\\r|<font.*?>|<!--.*?-->|<td.*?>|</td>|<tbody.*?>|</tbody>|</font>|<center>|<img.*?>|</img>|<stript.*?>|</stript>|<meta.*?>|</meta>|</center>|<a.*?>|</a>|<shapetype.*?/shapetype>|<strong.*?>|</strong>|<embed.*?/embed>|</br>|<xml>.*?<xml>|<?xml.*?>")
r_re = re.compile(r"(\\n)+|\n+")
br__re = re.compile(r"(<br>)+")
br_re = re.compile(r"<br.*?>")
s_re = re.compile(r"\s+")
p_re = re.compile(r"<p.*?>")
t_re = re.compile(r"(\\t)+|t311|\t2,736|t1")


def wash(line):
    newline=p_re.sub("<p>",line)
    newline=br_re.sub("<br>",newline)
    newline=br__re.sub("<br>",newline)
    newline=dorp_re.sub("",newline)
    newline=s_re.sub(r" ",newline)
    newline=t_re.sub(r"\\t",newline)
    newline=r_re.sub(r"\\n",newline)
    newline=r_re.sub(r"\\n",newline)
    return newline

class emptyPipeline(object):
    def process_item(self, item, spider):

        if item["novelId"]=="":
            raise DropItem("Duplicate tempry item ")
        else:
            return item



class mergePipeline(object):

    def __init__(self):
        self.title = dict()
        self.review=dict()
        self.time=dict()
        self.start=time.time()
        self.cnt=0

    def process_item(self, item, spider):
        nid=item["novelId"]


        if not nid in self.title:
            self.review[nid]={}
            self.title[nid]=item["title"]
            self.time[nid]=time.time()



        vid=int(item["volumeNo"])
        self.review[nid][vid]=item["review"]
        keys=self.review[nid].keys()



        if max(keys)==len(keys) and max(keys)>1:
            self.cnt+=1
            print self.cnt

            name=self.title.pop(nid)
            of=open("../../"+spider.name+"/"+name+".txt",'w+')

            cpt=dict()
            cpt["content"]=name
            for (v,c) in self.review[nid].items():
                cpt["review"]=wash(c)
                of.write(json.dumps(cpt, ensure_ascii=False)+"\n")
            self.review.pop(nid)
            self.time.pop(nid)
            raise DropItem("reivew")

        t=int(time.time()-self.start)
        if t%30==0:
            for i,volume in self.review.items():
                life=int(time.time()-self.time[i])
                if life>3000:
                    if max(volume.keys())==1:
                        kr=krItem()
                        kr["review"]=self.review[i][1]
                        kr["review"]=wash(kr["review"])
                        kr["content"]=self.title.pop(i)
                        self.review.pop(i)
                        self.time.pop(i)
                        self.cnt+=1
                        print self.cnt
                        return kr
        raise DropItem("reivew")






class KrPipeline(object):

    def open_spider(self, spider):
        os.mkdir("../../"+spider.name)
    def process_item(self, item, spider):
        name=itme["content"]
        of=open("../../"+spider.name+"/"+name+".txt",'w+')
        of.write(json.dumps(dict(item), ensure_ascii=False)+"\n")
