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



class YhPipeline(object):

    def open_spider(self, spider):
        self.client = MongoClient('spider02', 27017)
        self.buff=[]
        self.cnt=0
    def process_item(self, item, spider):
        dic=dict(item)

        if len(self.buff)<2:
            self.buff.append(dic)
        else:
            yh=self.client.yh.yh
            yh.insert_many(self.buff)
            self.buff=[]


class mergePipeline(object):
    def open_spider(self, spider):
        self.client = MongoClient('spider02', 27017)

    def process_item(self, item, spider):

        if "pid" in item:
            qid=item["qid"]
            review=item["review"]
            yh=self.client.yh.yh
            dic=yh.find_one({"qid":qid})
            try:
                new_review=dic["review"]+review
                print len(new_review)
            except BaseException,e:
                new_review=""
                print 0

            review=yh.update_one({'qid': qid}, {'$set': {'review': new_review}})
            raise DropItem("review")
        else:
            return item
