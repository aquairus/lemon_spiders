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

    #    print str(len(keys))+"/"+str(max(keys))



        if max(keys)==len(keys) and max(keys)>1:
            self.cnt+=1
            print self.cnt
            review=""
            for (v,c) in self.review[nid].items():
                review=review+c
            kr=krItem()
            kr["review"]=review
            kr["content"]=self.title.pop(nid)

            self.review.pop(nid)
            self.time.pop(nid)
            return kr

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
                # if life>36000:
                #     review=""
                #     for (v,c) in volume.items():
                #         review=review+c
                #     kr=krItem()
                #     kr["review"]=review
                #     kr["content"]=self.title.pop(i)
                #     self.review.pop(i)
                #     self.time.pop(i)
                #     print str(max(volume.keys()))+":"+str(len(volume))
                #     if len(volume)/max(volume.keys())>0.8:
                #         return kr





class KrPipeline(object):

    def open_spider(self, spider):
        self.of=open("../../"+spider.name+".txt",'w+')

    def process_item(self, item, spider):

        self.of.write(json.dumps(dict(item), ensure_ascii=False)+"\n")

    def close_spider(self, spider):
        self.of.close()
