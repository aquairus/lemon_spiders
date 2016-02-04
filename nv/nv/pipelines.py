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


class emptyPipeline(object):
    def process_item(self, item, spider):

        if item["content"]=="":
            raise DropItem("Duplicate tempry item ")
        else:
            return item

class NvPipeline(object):

    def open_spider(self, spider):
        self.of=open("../../nv.txt",'w+')

    def process_item(self, item, spider):

        self.of.write(json.dumps(dict(item), ensure_ascii=False)+"\n")

    def close_spider(self, spider):
        self.of.close()
