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

    def process_item(self, item, spider):
        nid=item["novelId"]

        if not nid in self.title:
            self.title[nid]=item["title"]

        if not nid in self.review:
            self.review[nid]={}


        if "volumeNo" in item:
            vid=int(item["volumeNo"])
            self.review[nid][vid]=item["review"]

            keys=self.review[nid].keys()

            print str(len(keys))+"/"+str(max(keys))

            if max(keys)==len(keys):
                print "finish"
                review=""
                for (v,c) in self.review[nid].items():
                    print v
                    review=review+c

                kr=krItem()
                kr["content"]=self.title[nid]
                kr["review"]=review
                return kr
            else:
                raise DropItem("reivew")



class KrPipeline(object):

    def open_spider(self, spider):
        self.of=open("../novel.txt",'w+')

    def process_item(self, item, spider):

        self.of.write(json.dumps(dict(item), ensure_ascii=False)+"\n")

    def close_spider(self, spider):
        self.of.close()
