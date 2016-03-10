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
from pymongo import MongoClient
import re





class xmPipeline(object):
    def open_spider(self, spider):

        self.of=open("../../"+spider.name+".txt",'w+')
        self.cnt=0




    def process_item(self, item, spider):
        self.cnt+=1
        print self.cnt        
        dic=dict(item)
        self.of.write(json.dumps(dic, ensure_ascii=False)+"\n")
