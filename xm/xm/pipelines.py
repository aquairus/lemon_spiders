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

        self.client = MongoClient('spider03', 27017)
        db=self.client.xm
        xm=db.get_collection(spider.name)
        xm.create_index("url")
        self.cnt=0




    def process_item(self, item, spider):
        self.cnt+=1
        print self.cnt
        dic=dict(item)
        db=self.client.xm
        xm=db.get_collection(spider.name)

        xm.insert_one(dic)



class contentPipeline(object):

    def process_item(self, item, spider):
        newline=item["content"]

        newline=p_re.sub("<p>",newline)
        newline=br_re.sub("<br>",newline)
        newline=br__re.sub("<br>",newline)
        newline=dorp_re.sub("",newline)
        newline=dorp2_re.sub("",newline)
        newline=s_re.sub(r" ",newline)
        newline=t_re.sub(r"\\t",newline)
        newline=r_re.sub(r"\\n",newline)
        newline=r_re.sub(r"\\n",newline)

        item["content"]=newline
        return item
