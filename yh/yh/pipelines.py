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
        qid=item["qid"]
        yh=self.client.yh.yh
        dic=dict(item)

        review=yh.find_one_and_delete({"qid":qid})

        if review:
            dic["review"]=review["review"]+dic["review"]
        yh.insert_one(dic)



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
                yh.update_one({'qid': qid}, {'$set': {'review': new_review}})
            except BaseException,e:
                review=dict(item)
                yh.insert_one(review)
            raise DropItem("review")
        else:
            return item
