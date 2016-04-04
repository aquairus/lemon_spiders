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



class mergePipeline(object):

    def __init__(self):
        self.content = dict()
        self.dis=dict()

    def process_item(self, item, spider):
        bid=item["bid"]

        if "title" in item:
            self.content[bid]=item
            raise DropItem("content")
        else:
            sf=self.content[bid].copy()
            self.content.pop(bid)
            sf["dis"]=item["dis"]
            return sf


class sfPipeline(object):

    def open_spider(self, spider):
        self.of=open("../sf.txt",'w+')
        self.cnt=0

    def process_item(self, item, spider):
        self.cnt+=1
        print self.cnt
        self.of.write(json.dumps(dict(item), ensure_ascii=False)+"\n")

    def close_spider(self, spider):
        self.of.close()
