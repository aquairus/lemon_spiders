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
                cpt["review"]=c
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
